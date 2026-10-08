import json

from web_app import app, assistant


if __name__ == "__main__":
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
