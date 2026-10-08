# AGENTS.md — Asistente Experto basado en RAG
Sistema de IA capaz de "leer" manuales técnicos de soporte de Nintendo (PDFs), responder preguntas y realizar tareas sobre ellos usando RAG sin entregar el corpus completo a un modelo externo.

## Stack y estructura
- **Python**: Lenguaje principal del backend y pipeline RAG.
- **Flask**: Utilizado para la interfaz conversacional web (`web_app.py`).
- `src/`: Lógica del RAG y pipeline principal (`assistant.py`, `config.py`, `knowledge.py`, `prompt_templates.py`).
- `data/manuales/`: Corpus de documentos a procesar.
- `docs/`: Documentación y diagramas del proyecto.
- `scripts/`: Scripts auxiliares.
- `main.py` / `web_app.py`: Puntos de entrada para el script RAG y la app web.
- `index.html`: Frontend del chat web.

## Comandos
- Para activar el entorno virtual (Windows): `.venv\Scripts\activate`
- Para instalar dependencias: `pip install -r requirements.txt`
- Para ejecutar la aplicación web: `python web_app.py`
- Para ejecutar el backend RAG: `python main.py`

## Convenciones
- Estilo de código PEP 8.
- Usar variables de entorno (`.env`) para todas las credenciales de API.
- Mantener siempre la justificación de decisiones en el README (chunking, embeddings, etc.).

## Reglas de dominio / trampas conocidas
- Nunca enviar documentos completos al LLM, solo fragmentos recuperados.
- El LLM debe citar explícitamente la fuente (documento y fragmento) de cada respuesta, usando metadatos.
- Manejar explícitamente los casos donde la información no esté en el corpus para controlar las alucinaciones.

## Forma de trabajar
- Antes de modificar el pipeline RAG (chunking, embeddings, prompts), planificar el impacto en las métricas de evaluación (Ragas).
- Documentar al menos una iteración de mejora tras la evaluación.

## Límites
- ✅ Siempre: actualizar `MEMORY.md` al terminar cada tarea.
- ✅ Siempre: mantener el formato de salida y citas del System Prompt (definidos en el Avance 1).
- ⚠️ Pregunta antes: agregar nuevas librerías pesadas al `requirements.txt` o cambiar el framework web/base de datos vectorial.
- 🚫 Nunca: subir `.env` o secretos/API keys reales al repositorio.

## Verificación
- Validar consultas exitosas y fallidas (fuera del corpus) en la interfaz.
- Ejecutar el script de evaluación con Ragas y verificar las métricas: `faithfulness`, `answer_relevancy`, `context_precision` y `context_recall`.
- Asegurar que la interfaz web sea capaz de mantener el historial de diálogo (preguntas de seguimiento).

## Memoria
- Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y las decisiones tomadas.
- Al terminar una tarea, actualízalo: estado actual, decisiones importantes (con su porqué) y errores a evitar.
- Mantenlo breve (máximo ~50 líneas): resume o elimina lo que ya no aporte.
- Si algo se convierte en una regla permanente, propón moverlo a `AGENTS.md` en lugar de dejarlo en la memoria.
- No guardes nunca datos sensibles (claves, tokens, datos personales).
