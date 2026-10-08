from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from src.assistant import SupportAssistant


ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
assistant = SupportAssistant()


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "")
    history = payload.get("history", [])

    if not isinstance(question, str):
        return jsonify({"error": "La pregunta debe ser texto."}), 400

    try:
        return jsonify(assistant.answer(question, history=history))
    except Exception:
        app.logger.exception("Error al procesar la consulta")
        return jsonify({"error": "No se pudo procesar la consulta."}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
