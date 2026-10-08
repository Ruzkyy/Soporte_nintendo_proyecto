from pathlib import Path
from typing import List, Dict

def load_manuals(folder_path: Path) -> List[Dict[str, str]]:
    """
    Carga documentos (PDF o TXT) y devuelve una lista de diccionarios.
    Cada diccionario contiene 'source' (nombre del archivo) y 'content' (texto completo).
    """
    docs = []
    if not folder_path.exists():
        return docs

    for file_path in sorted(folder_path.glob("*.*")):
        content = ""
        try:
            if file_path.suffix.lower() == ".pdf":
                # Usar pypdf para archivos PDF
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                text_parts = []
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_parts.append(extracted)
                content = "\n".join(text_parts)
            else:
                # Leer como texto plano
                content = file_path.read_text(encoding="utf-8")
                
            if content.strip():
                docs.append({
                    "source": file_path.name,
                    "content": content
                })
        except Exception as e:
            print(f"Error cargando {file_path.name}: {e}")
            continue
            
    return docs
