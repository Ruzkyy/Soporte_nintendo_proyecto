# Switch Care: Asistente de Soporte para Nintendo Switch 2

## Autores

- Julian Arley Ruiz Gonzalez
- Luna Anahy Chaparro Bustos

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

## Instalación desde Git Bash

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone https://github.com/Ruzkyy/Soporte_nintendo_proyecto.git
cd Soporte_nintendo_proyecto
```

Crea o activa el entorno virtual. Si el repositorio ya incluye un entorno local
en tu equipo, actívalo; de lo contrario, créalo:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de la API

Copia el archivo de ejemplo y edítalo con tu clave personal:

```bash
cp .env.example .env
```

El archivo `.env` debe contener:

```env
GEMINI_API_KEY=tu_clave_de_gemini
GEMINI_MODEL=gemini-3.6-flash
```

No subas `.env` a GitHub ni compartas su contenido. `.gitignore` ya excluye
ese archivo. Si no configuras la clave, el programa funciona en modo
demostración y muestra el contexto local recuperado.

## Ejecución en consola

```bash
python main.py
```

Escribe una consulta y presiona Enter. Para terminar, escribe `salir`.

Ejemplo de pregunta:

```text
Pregunta> Mi Nintendo Switch 2 no enciende
```

## Ejecución de la interfaz web

Con el entorno virtual activo, ejecuta:

```bash
python web_app.py
```

Después abre `http://127.0.0.1:5000` en el navegador. La interfaz envía las
preguntas al endpoint `/api/chat`.

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

## Flujo de procesamiento

1. `src/config.py` carga las variables de `.env`.
2. `src/knowledge.py` lee el manual local y recupera los fragmentos relevantes.
3. `src/prompt_templates.py` construye el prompt con reglas, ejemplos y etiquetas XML.
4. `src/assistant.py` envía la pregunta y el contexto al modelo configurado.
5. La respuesta se limpia y se entrega en formato JSON.

## Objetivo del proyecto

Este repositorio implementa el avance de diseño de prompts y un prototipo RAG
para soporte técnico. Define las instrucciones del sistema, integra ejemplos de
respuesta, utiliza delimitadores XML y recupera información desde un manual
local.

## Privacidad y alcance

El manual y la recuperación de información se procesan localmente. Si se
configura `GEMINI_API_KEY`, la pregunta y los fragmentos recuperados se envían
a la API de Gemini. Para un funcionamiento completamente local sería necesario
sustituir ese cliente por un modelo instalado en el equipo.
