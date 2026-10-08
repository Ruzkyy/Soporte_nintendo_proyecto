from typing import List

def split_text_with_overlap(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Divide un texto en fragmentos (chunks) basándose en la cantidad de palabras,
    manteniendo un solapamiento (overlap) para no perder contexto.
    """
    words = text.split()
    chunks = []
    
    if not words:
        return chunks

    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        
        # Avanzar el índice restando el overlap
        i += (chunk_size - overlap)
        
        # Si el avance no mueve el índice (en caso de overlap anómalo), forzamos avance
        if chunk_size - overlap <= 0:
            i += chunk_size
            
    return chunks
