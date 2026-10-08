import json
from typing import Any, List, Dict

from google import genai
from google.genai import types

from src.config import settings
from src.vector_store import VectorStore
from src.prompt_templates import SYSTEM_PROMPT, build_user_prompt


RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "resumen": {"type": "STRING"},
        "diagnostico": {"type": "STRING"},
        "pasos": {"type": "ARRAY", "items": {"type": "STRING"}},
        "solucion_recomendada": {"type": "STRING"},
        "nivel_confianza": {
            "type": "STRING",
            "enum": ["alta", "media", "baja"],
        },
    },
    "required": [
        "resumen",
        "diagnostico",
        "pasos",
        "solucion_recomendada",
        "nivel_confianza",
    ],
}


class SupportAssistant:
    def __init__(self):
        self.vector_store = VectorStore(
            persist_dir=settings.VECTOR_DB_DIR, 
            data_dir=settings.KNOWLEDGE_DIR
        )
        self.client = None
        if settings.API_KEY:
            self.client = genai.Client(api_key=settings.API_KEY)

    def _clean_json_response(self, raw_text: str) -> dict[str, Any]:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            if start < 0:
                parsed = None
            else:
                try:
                    parsed, _ = json.JSONDecoder().raw_decode(cleaned[start:])
                except json.JSONDecodeError:
                    parsed = None

        if isinstance(parsed, dict):
            required_fields = {
                "resumen",
                "diagnostico",
                "pasos",
                "solucion_recomendada",
                "nivel_confianza",
            }
            if required_fields.issubset(parsed) and isinstance(parsed["pasos"], list):
                return parsed

        raise ValueError("El modelo devolvió una respuesta incompleta o con formato JSON inválido.")

    def _fallback_response(self, question: str, context: str) -> dict[str, Any]:
        return {
            "resumen": f"Se recibió la consulta: {question}",
            "diagnostico": "No hay clave de API activa en la configuración. La respuesta se devuelve en modo de demostración.",
            "pasos": [
                "Revisa el archivo .env y agrega GEMINI_API_KEY.",
                "Consulta la documentación del manual local.",
                "Vuelve a ejecutar el asistente con una pregunta concreta."
            ],
            "solucion_recomendada": "Configura la API para obtener una respuesta real del modelo.",
            "nivel_confianza": "baja",
            "contexto_utilizado": context,
        }

    def format_history(self, history: List[Dict[str, str]]) -> str:
        if not history:
            return ""
        formatted = []
        for msg in history:
            role = "Usuario" if msg.get("role") == "user" else "Asistente"
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)

    def answer(self, question: str, history: List[Dict[str, str]] = None) -> dict[str, Any]:
        if not question or not question.strip():
            return {
                "resumen": "La pregunta está vacía.",
                "diagnostico": "No se puede evaluar un problema sin descripción.",
                "pasos": [],
                "solucion_recomendada": "Escribe el problema técnico con detalles del equipo, error y contexto.",
                "nivel_confianza": "baja",
                "fuentes": []
            }

        # 1. Recuperar contexto de la base de datos vectorial FAISS
        retrieved_items = self.vector_store.retrieve(question, top_k=5)
        
        context_blocks = []
        fuentes = []
        for item in retrieved_items:
            source = item["metadata"]["source"]
            chunk_index = item["metadata"]["chunk_index"]
            text = item["chunk"]
            context_blocks.append(f"Fuente: {source} (fragmento {chunk_index})\n{text}")
            
            # Guardar fuentes para la UI
            fuente_str = f"{source} (frag. {chunk_index})"
            if fuente_str not in fuentes:
                fuentes.append(fuente_str)

        context_str = "\n\n---\n\n".join(context_blocks) if context_blocks else "No hay contexto disponible en la base de conocimientos local."
        
        # 2. Formatear historial
        history_str = self.format_history(history)

        # 3. Construir prompt
        prompt = build_user_prompt(question, context_str, history_str)

        if not self.client:
            resp = self._fallback_response(question, context_str)
            resp["fuentes"] = fuentes
            return resp

        # 4. Generar respuesta probando modelos (Fallback)
        models_to_try = [settings.MODEL] + settings.FALLBACK_MODELS
        last_exception = None

        for current_model in models_to_try:
            try:
                print(f"Intentando generar respuesta con el modelo: {current_model}")
                response = self.client.models.generate_content(
                    model=current_model,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2,
                        max_output_tokens=1024,
                        response_mime_type="application/json",
                        response_schema=RESPONSE_SCHEMA,
                    ),
                    contents=prompt,
                )
                parsed_json = self._clean_json_response(response.text)
                parsed_json["fuentes"] = fuentes  # Inyectar fuentes al JSON final
                return parsed_json
            except Exception as exc:
                print(f"Error con el modelo {current_model}: {exc}")
                last_exception = exc
                continue # Probar con el siguiente modelo
                
        # Si todos los modelos fallan:
        return {
            "resumen": f"No se pudo completar la respuesta para: {question}",
            "diagnostico": f"Todos los modelos fallaron. Último error: {last_exception}",
            "pasos": [
                "Verifica tu conexión a internet.",
                "Espera unos minutos si los servidores están bajo alta demanda (503).",
                "Asegúrate de que tu API Key de Gemini sea válida y tenga permisos."
            ],
            "solucion_recomendada": "Vuelve a intentarlo en unos minutos.",
            "nivel_confianza": "baja",
            "fuentes": []
        }
