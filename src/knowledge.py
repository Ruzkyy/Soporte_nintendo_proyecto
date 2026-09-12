from pathlib import Path
import re


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def load_manuals(folder: Path):
    docs = []
    if not folder.exists():
        return docs

    for path in sorted(folder.glob("*.*")):
        try:
            content = path.read_text(encoding="utf-8")
            if content.strip():
                docs.append({"source": path.name, "content": content})
        except Exception:
            continue
    return docs


def split_into_chunks(text: str, chunk_size: int = 400) -> list[str]:
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


def retrieve_context(question: str, documents: list, limit: int = 3) -> str:
    if not documents:
        return "No hay contexto disponible en la base de conocimientos local."

    query_tokens = set(re.findall(r"[a-z0-9]+", normalize_text(question)))
    ranked = []

    for document in documents:
        chunks = split_into_chunks(document["content"])
        for index, chunk in enumerate(chunks):
            chunk_text = normalize_text(chunk)
            score = sum(1 for token in query_tokens if token in chunk_text)
            if score > 0:
                ranked.append({
                    "source": document["source"],
                    "chunk": chunk,
                    "score": score,
                    "index": index,
                })

    ranked.sort(key=lambda item: item["score"], reverse=True)

    selected = ranked[:limit]
    if not selected:
        return "No se encontraron coincidencias relevantes en el manual del soporte técnico."

    context_blocks = [
        f"Fuente: {item['source']}\n{item['chunk']}"
        for item in selected
    ]
    return "\n\n---\n\n".join(context_blocks)
