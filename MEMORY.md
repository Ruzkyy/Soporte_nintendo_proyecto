# MEMORY.md — Diario de Estudio
Memoria del proyecto entre sesiones. Máximo ~50 líneas.

## Estado actual
- Backend RAG modular con FAISS persistente en `data/vector_db/`.
- Embeddings: `paraphrase-multilingual-MiniLM-L12-v2`.
- La app web mantiene historial conversacional y muestra fuentes recuperadas.
- UI `index.html` con marco Switch 2; los Joy-Con CSS usan carcasas grafito a toda altura, colores hacia el centro y sticks asimétricos. En móvil se simplifican para preservar el chat.
- README actualizado para reflejar arquitectura Flask/RAG/FAISS y documentar configuración, endpoint, privacidad y límites de evaluación.
- Evaluación configurada con Ragas en `scripts/evaluate_rag.py`.

## Decisiones
- PDFs se cargan con `pypdf` y se dividen en fragmentos de 300 palabras con solapamiento de 50.
- Respuestas solo reciben fragmentos recuperados; conservar citas por documento y fragmento.

## Aprendizajes y errores a evitar
- La recuperación combina distancia FAISS con coincidencia léxica normalizada (sin tildes y con prefijos) para evitar perder términos exactos en consultas en español.
- `SupportAssistant.answer()` recupera cinco fragmentos y solicita JSON con esquema a Gemini; el parser acepta JSON rodeado de texto.
- El prompt pide responder en el idioma del usuario y comprender faltas ortográficas; se verificó en vivo `La camra como la conecto?`.
- La cámara requiere `NSwitch2_Information_Camera_EUR.pdf`.
- Los fallbacks Gemini vigentes son `gemini-3.5-flash` y `gemini-3.5-flash-lite`; no volver a usar modelos retirados como `gemini-1.0-pro` o `gemini-2.5-flash-lite`.
- Los atajos de consultas frecuentes deben enviar una pregunta; las fuentes deben mantenerse legibles en pantallas estrechas.
- `scripts/evaluate_rag.py` aún referencia `gemini-1.5-flash`; la evaluación Ragas no está validada hasta actualizar ese evaluador.
- `data/vector_db/metadata.json` es el índice activo; los manuales ya indexados no requieren reconstrucción para estas correcciones.

## Próximos pasos
- Evaluar `faithfulness`, `answer_relevancy`, `context_precision` y `context_recall`.
- Probar consultas exitosas, fuera del corpus y seguimientos conversacionales en la UI.
- Preparar capturas y despliegue final.
