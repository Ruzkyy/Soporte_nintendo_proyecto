import json
import os
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.loaders import load_manuals
from src.splitters import split_text_with_overlap


def _normalized_terms(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return set(re.findall(r"[a-z0-9]+", normalized))


class VectorStore:
    def __init__(self, persist_dir: Path, data_dir: Path):
        self.persist_dir = persist_dir
        self.data_dir = data_dir
        
        # Crear directorio si no existe
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_path = self.persist_dir / "faiss_index.bin"
        self.meta_path = self.persist_dir / "metadata.json"
        
        print("Cargando modelo de embeddings (esto puede tomar unos segundos la primera vez)...")
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        self.index = None
        self.metadata = []
        
        if self.index_path.exists() and self.meta_path.exists():
            self._load_store()
        else:
            self._populate()

    def _load_store(self):
        """Carga el índice FAISS y los metadatos desde el disco."""
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def _populate(self):
        """Carga documentos, los divide, genera embeddings y guarda en FAISS."""
        print("Poblando la base de datos vectorial FAISS localmente...")
        docs = load_manuals(self.data_dir)
        
        if not docs:
            print("No se encontraron documentos para poblar la base de datos.")
            return

        texts = []
        self.metadata = []
        
        chunk_id_counter = 0
        
        for doc in docs:
            chunks = split_text_with_overlap(doc["content"], chunk_size=300, overlap=50)
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                self.metadata.append({
                    "id": chunk_id_counter,
                    "chunk": chunk,
                    "metadata": {"source": doc["source"], "chunk_index": i}
                })
                chunk_id_counter += 1
                
        if not texts:
            return

        # Generar embeddings
        print(f"Generando embeddings para {len(texts)} fragmentos...")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Inicializar FAISS (L2 distance)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Guardar en disco
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
        print("Base de datos vectorial creada y guardada con éxito.")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Recupera fragmentos relevantes combinando similitud y coincidencia léxica."""
        if not self.index or len(self.metadata) == 0:
            return []
            
        # Generar embedding de la pregunta
        query_vector = self.model.encode([query], convert_to_numpy=True)
        
        # Puntuar todos los fragmentos permite recuperar términos exactos que el embedding ordena mal.
        distances, indices = self.index.search(query_vector, len(self.metadata))
        stop_words = {"como", "con", "de", "del", "el", "la", "las", "los", "para", "por", "que", "un", "una"}
        query_terms = _normalized_terms(query) - stop_words
        
        ranked_chunks = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                chunk_terms = _normalized_terms(item["chunk"])
                matches = sum(
                    term in chunk_terms
                    or (len(term) >= 5 and any(word.startswith(term[:5]) for word in chunk_terms))
                    for term in query_terms
                )
                lexical_score = matches / len(query_terms) if query_terms else 0
                ranked_chunks.append((lexical_score, float(dist), item))

        ranked_chunks.sort(key=lambda result: (-result[0], result[1]))
        return [
            {
                "chunk": item["chunk"],
                "metadata": item["metadata"],
                "distance": distance,
            }
            for _, distance, item in ranked_chunks[:top_k]
        ]
