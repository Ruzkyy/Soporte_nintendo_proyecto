import json
from typing import Any

from google import genai
from google.genai import types

from src.config import settings
from src.knowledge import load_manuals, retrieve_context
from src.prompt_templates import SYSTEM_PROMPT, build_user_prompt


class SupportAssistant:
    def __init__(self):
        self.documents = load_manuals(settings.KNOWLEDGE_DIR)
        self.client = None
        if settings.API_KEY:
            self.client = genai.Client(api_key=settings.API_KEY)

    def _clean_json_response(self, raw_text: str) -> dict[str, Any]:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                "resumen": cleaned[:200],
                "diagnostico": "La respuesta no llegó en formato JSON válido.",
                "pasos": [],
                "solucion_recomendada": "Solicita la respuesta nuevamente con una pregunta más específica.",
                "nivel_confianza": "baja",
            }

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

    def answer(self, question: str) -> dict[str, Any]:
        if not question or not question.strip():
            return {
                "resumen": "La pregunta está vacía.",
                "diagnostico": "No se puede evaluar un problema sin descripción.",
                "pasos": [],
                "solucion_recomendada": "Escribe el problema técnico con detalles del equipo, error y contexto.",
                "nivel_confianza": "baja",
            }

        context = retrieve_context(question, self.documents, limit=3)
        prompt = build_user_prompt(question, context)

        if not self.client:
            return self._fallback_response(question, context)

        try:
            response = self.client.models.generate_content(
                model=settings.MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=1024,
                ),
                contents=prompt,
            )
            return self._clean_json_response(response.text)
        except Exception as exc:
            return {
                "resumen": f"No se pudo completar la respuesta para: {question}",
                "diagnostico": str(exc),
                "pasos": [
                    "Verifica la API key de Gemini.",
                    "Asegúrate de que el modelo exista en tu cuenta.",
                    "Reintenta la consulta con una pregunta más específica."
                ],
                "solucion_recomendada": "Revisa la configuración de acceso y la disponibilidad del modelo.",
                "nivel_confianza": "baja",
            }
