import json

from src.assistant import SupportAssistant


if __name__ == "__main__":
    assistant = SupportAssistant()
    print("Asistente de Soporte Técnico")
    print("Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("Pregunta> ").strip()
        if pregunta.lower() in {"salir", "exit", "finalizar"}:
            print("Hasta luego.")
            break

        respuesta = assistant.answer(pregunta)
        print(json.dumps(respuesta, ensure_ascii=False, indent=2))
        print()
