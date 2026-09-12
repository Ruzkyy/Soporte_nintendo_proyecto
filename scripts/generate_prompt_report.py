from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "prompt_execution_report.pdf"


def add_title(pdf, text):
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(25 * mm, 270 * mm, text)


def add_section(pdf, title, text, y_pos):
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, y_pos, title)
    pdf.setFont("Helvetica", 10)
    wrapped = pdf.beginText(25 * mm, y_pos - 12)
    lines = text.split("\n")
    for line in lines:
        wrapped.textLine(line)
    pdf.drawText(wrapped)


def generate_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4)

    pdf.setTitle("Reporte del prompt del asistente de soporte técnico")
    pdf.setAuthor("Proyecto académico")

    pdf.setFillColorRGB(0.12, 0.18, 0.31)
    pdf.rect(15 * mm, 255 * mm, 180 * mm, 30 * mm, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(25 * mm, 268 * mm, "Asistente de Soporte Técnico")

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, 235 * mm, "1. Definición del prompt")
    pdf.setFont("Helvetica", 10)
    text = (
        "El system prompt define el rol del modelo, sus reglas y el formato de respuesta. "
        "El asistente actúa como analista técnico senior y responde con JSON.\n"
        "La recuperación y el manual se mantienen locales; con GEMINI_API_KEY, "
        "la pregunta y el contexto recuperado se envían a Gemini."
    )
    wrapped = pdf.beginText(25 * mm, 220 * mm)
    for line in text.split(" "):
        wrapped.textLine(line)
    pdf.drawText(wrapped)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, 195 * mm, "2. Ejemplo Few-Shot")
    pdf.setFont("Helvetica", 9)
    example = (
        "Pregunta: Mi equipo no enciende.\n"
        "Respuesta: {\"resumen\":\"El equipo no enciende\",\"diagnostico\":\"Falla de alimentación\",\"pasos\":[\"Verificar cable\",\"Comprobar fuente\"],\"solucion_recomendada\":\"Revisar alimentación\",\"nivel_confianza\":\"alta\"}"
    )
    wrapped = pdf.beginText(25 * mm, 180 * mm)
    for line in example.split("\n"):
        wrapped.textLine(line)
    pdf.drawText(wrapped)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, 135 * mm, "3. Delimitadores")
    pdf.setFont("Helvetica", 9)
    delimiters = (
        "<instrucciones> ... </instrucciones>\n"
        "<contexto> ... </contexto>\n"
        "<pregunta> ... </pregunta>"
    )
    wrapped = pdf.beginText(25 * mm, 120 * mm)
    for line in delimiters.split("\n"):
        wrapped.textLine(line)
    pdf.drawText(wrapped)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, 80 * mm, "4. Flujo en RAG")
    pdf.setFont("Helvetica", 9)
    flow = (
        "Pregunta del usuario -> Búsqueda local -> Contexto relevante -> Prompt + reglas + ejemplos -> Respuesta estructurada"
    )
    pdf.drawString(25 * mm, 66 * mm, flow)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(25 * mm, 40 * mm, "5. Configuración y ejecución")
    pdf.setFont("Helvetica", 9)
    setup = (
        "1. Copiar .env.example como .env.\n"
        "2. Agregar GEMINI_API_KEY y GEMINI_MODEL.\n"
        "3. Instalar: pip install -r requirements.txt.\n"
        "4. Ejecutar: python main.py o python web_app.py.\n"
        "5. Consultar: Mi Nintendo Switch 2 no enciende.\n"
        "6. Verificar una respuesta JSON estructurada."
    )
    wrapped = pdf.beginText(25 * mm, 28 * mm)
    for line in setup.split("\n"):
        wrapped.textLine(line)
    pdf.drawText(wrapped)

    pdf.showPage()
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(25 * mm, 270 * mm, "6. Diagrama y resultado esperado")
    pdf.rect(35 * mm, 95 * mm, 35 * mm, 18 * mm)
    pdf.drawString(41 * mm, 101 * mm, "Usuario")
    pdf.rect(100 * mm, 95 * mm, 45 * mm, 18 * mm)
    pdf.drawString(108 * mm, 101 * mm, "RAG")
    pdf.rect(170 * mm, 95 * mm, 40 * mm, 18 * mm)
    pdf.drawString(176 * mm, 101 * mm, "IA")
    pdf.line(70 * mm, 104 * mm, 100 * mm, 104 * mm)
    pdf.line(145 * mm, 104 * mm, 170 * mm, 104 * mm)
    pdf.drawString(84 * mm, 115 * mm, "Pregunta")
    pdf.drawString(156 * mm, 115 * mm, "Contexto")
    pdf.drawString(119 * mm, 80 * mm, "Respuesta JSON")
    pdf.line(125 * mm, 95 * mm, 125 * mm, 80 * mm)

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(25 * mm, 55 * mm, "Resultado de ejemplo")
    pdf.setFont("Courier", 8)
    pdf.drawString(25 * mm, 45 * mm, '{"resumen":"La consola no enciende", "nivel_confianza":"alta"}')

    pdf.showPage()
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(25 * mm, 270 * mm, "7. Evidencia de ejecución")
    pdf.setFont("Helvetica", 10)
    evidence = (
        "La ejecución se realiza desde la terminal o desde la interfaz web local.\n\n"
        "> python main.py\n"
        "Asistente de Soporte Técnico\n"
        "> Pregunta> Mi Nintendo Switch 2 no enciende\n"
        "> {\"resumen\": \"La consola no enciende\", ...}\n\n"
        "La interfaz web se inicia con python web_app.py y queda disponible en\n"
        "http://127.0.0.1:5000. Se recomienda añadir capturas de la ejecución real\n"
        "a la entrega final junto con este reporte."
    )
    wrapped = pdf.beginText(25 * mm, 245 * mm)
    for line in evidence.split("\n"):
        wrapped.textLine(line)
    pdf.drawText(wrapped)

    pdf.save()
    print(f"PDF generado en: {OUTPUT}")


if __name__ == "__main__":
    generate_pdf()
