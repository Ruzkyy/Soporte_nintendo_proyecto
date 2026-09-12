# Switch Care: Asistente de Soporte para Nintendo Switch 2

Este proyecto es una propuesta académica de asistente experto para orientar incidencias de Nintendo Switch 2. Está diseñado para responder preguntas sobre encendido, carga, conexión, juegos, controles, temperatura, seguridad y buenas prácticas de soporte.

La solución combina:

- System prompts para definir rol, reglas y comportamiento del asistente.
- Few-shot prompting para mostrar ejemplos de respuesta en formato estructurado.
- Delimitadores XML para separar instrucciones, contexto de conocimiento y pregunta del usuario.
- Recuperación de contexto (RAG simple) sobre un manual técnico local.
- Formato de salida JSON para que la respuesta sea consistente y fácil de integrar.

## Enfoque del proyecto

Se trabaja con el enfoque de "Analista de Soporte Técnico". El asistente debe:

- detectar el problema técnico y resumirlo;
- sugerir diagnósticos o causas probables;
- proponer pasos de solución ordenados;
- indicar nivel de prioridad o riesgo;
- responder en español de forma clara, útil y profesional.

## Estructura del proyecto

```text
analista-soporte-tecnico/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
├── web_app.py
├── index.html
├── data/
│   └── manuales/
│       └── manual_soporte_it.txt
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── knowledge.py
│   ├── prompt_templates.py
│   └── assistant.py
├── scripts/
│   └── generate_prompt_report.py
└── docs/
    └── prompt_execution_report.pdf
```

## Cómo funciona

### 1. System Prompt

El modelo recibe instrucciones del sistema que definen su identidad y comportamiento:

- eres un analista de soporte técnico senior;
- respondes en español;
- usas solo el contexto disponible;
- si no hay contexto suficiente, lo indicas claramente;
- entregas una salida estructurada en JSON.

### 2. Few-Shot Prompting

Se incluyen varios ejemplos de preguntas y respuestas esperadas para enseñar el formato de salida:

```json
{
  "resumen": "El usuario reporta que el equipo no enciende.",
  "diagnostico": "Puede haber fallo de alimentación o consumo inicial.",
  "pasos": [
    "Verificar el cable de energía.",
    "Comprobar si el botón de encendido funciona.",
    "Probar otra toma eléctrica."
  ],
  "solucion_recomendada": "Revisar fuente de alimentación y cable.",
  "nivel_confianza": "alta"
}
```

### 3. Delimitadores

Las instrucciones y el contexto se separan con etiquetas XML para reducir ambigüedad:

```xml
<instrucciones>
... reglas del asistente ...
</instrucciones>

<contexto>
... fragmentos del manual ...
</contexto>

<pregunta>
... pregunta del usuario ...
</pregunta>
```

### 4. RAG simple

El sistema busca fragmentos relevantes dentro del manual técnico local y los incorpora al prompt antes de pedir la respuesta final.

## Configuración

El repositorio no incluye ninguna clave privada. Crea un archivo `.env` local a
partir de `.env.example` y agrega tu propia clave de Gemini:

```env
GEMINI_API_KEY=tu_clave
GEMINI_MODEL=gemini-3.6-flash
```

No publiques `.env`, no compartas la clave por capturas y revoca cualquier clave
que haya quedado expuesta. El archivo `.gitignore` ya excluye `.env`.

## Instalación

```bash
cd analista-soporte-tecnico
python -m venv venv
source venv/bin/activate   # Linux/Mac
# o .\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Ejecución paso a paso

```bash
python main.py
```

1. `src/config.py` carga las variables de `.env`.
2. `src/knowledge.py` lee el manual local y recupera los fragmentos con mayor coincidencia.
3. `src/prompt_templates.py` construye el prompt con reglas, ejemplos few-shot y etiquetas XML.
4. `src/assistant.py` envía el contexto al modelo configurado y valida la respuesta JSON.
5. Si no existe `GEMINI_API_KEY`, se ejecuta un modo demostración sin realizar llamadas externas.

Ejemplo de pregunta:

```text
Pregunta> Mi Nintendo Switch 2 no enciende
```

## Ejecución de la interfaz web

Instala las dependencias y ejecuta el servidor web:

```bash
pip install -r requirements.txt
python web_app.py
```

Después abre `http://127.0.0.1:5000` en el navegador. La interfaz envía las
preguntas a `/api/chat`, donde se utiliza `SupportAssistant`, el manual local,
el RAG y Gemini configurado en `.env`.

Ejemplo de interacción:

```text
Pregunta> Mi PC se reinicia sola al abrir la aplicación de edición
```

## Salida esperada

El asistente responde con un JSON estructurado:

```json
{
  "resumen": "El problema se presenta durante la apertura de una aplicación de edición.",
  "diagnostico": "Podría tratarse de un problema de temperatura, memoria o driver gráfico.",
  "pasos": [
    "Verificar temperatura del equipo.",
    "Revisar drivers del GPU.",
    "Comprobar uso de memoria RAM."
  ],
  "solucion_recomendada": "Actualizar controladores y validar que no haya sobrecalentamiento.",
  "nivel_confianza": "media"
}
```

## Generación del PDF explicativo

Se incluye un script que genera un reporte PDF con:

- explicación del prompt;
- esquema de flujo del asistente;
- ejemplo de few-shot;
- diagrama del proceso de RAG;
- notas de ejecución.

```bash
python scripts/generate_prompt_report.py
```

El archivo generado en `docs/prompt_execution_report.pdf` documenta el prompt,
el few-shot, los delimitadores, el flujo RAG, la configuración del `.env` y un
ejemplo de ejecución. Para una entrega formal se recomienda acompañarlo con
capturas de la terminal y de la interfaz web mostrando una consulta real.

## Objetivo académico

Este repositorio cumple con el avance 1 del proyecto de IA aplicada: define claramente la estructura de instrucciones del sistema, integra ejemplos de respuesta, utiliza delimitadores para separar contenido y prepara la base para un sistema RAG más completo con agentes.

## Nota de privacidad y alcance

Los documentos y la recuperación de contexto se procesan localmente. Cuando se
configura `GEMINI_API_KEY`, la pregunta y los fragmentos recuperados se envían a
la API de Gemini, por lo que esta versión no es completamente local. Para una
privacidad total debe sustituirse el cliente de Gemini por un modelo local. El
proyecto implementa un asistente RAG de un solo flujo; no incluye todavía una
arquitectura multiagente autónoma.

## Publicación en GitHub

Después de crear tu `.env` local, publica únicamente los archivos del proyecto:

```bash
git init
git add .
git commit -m "Entrega inicial del asistente RAG de soporte"
git branch -M main
git remote add origin https://github.com/Ruzkyy/Soporte_nintendo_proyecto.git
git push -u origin main
```

Antes de hacer `push`, verifica que `.env` no aparezca en `git status`.
