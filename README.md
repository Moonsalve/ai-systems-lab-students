# Lab 03 — Asistente con tools y un servidor MCP

Tercera versión del Asistente Inteligente del Curso de IA (`Usuario → Asistente → LLM + Tools`):
el LLM pide herramientas (tools locales y de un servidor MCP), el programa las valida, pide
confirmación para las acciones con efectos y las ejecuta.

Basado en [ProfOmarPinzon/ai-systems-lab-students](https://github.com/ProfOmarPinzon/ai-systems-lab-students).
Incluye `labs/02-rag` solo para la comparación del Paso 0.

## Requisitos

- Python 3.11 o superior y [uv](https://docs.astral.sh/uv/)
- Una API key de un proveedor compatible con Chat Completions y un modelo con **tool calling**
  (las pruebas se hicieron con Groq · `qwen/qwen3.8-27b`)

## Configuración

```bash
uv sync
cp .env.example .env        # Windows (PowerShell): Copy-Item .env.example .env
```

Completa `LLM_PROVIDER`, `LLM_API_KEY` y `LLM_MODEL` en `.env`. El archivo `.env` está en
`.gitignore` y no forma parte del repositorio.

## Ejecución (desde la raíz)

```bash
uv run python labs/03-mcp/tools.py                         # tools locales, sin LLM
uv run python labs/03-mcp/tool_calling.py "¿Qué día es hoy?"  # el modelo genera, no ejecuta
uv run python labs/03-mcp/mcp_client.py                    # cliente MCP, sin LLM
uv run python labs/03-mcp/chatbot.py --debug               # asistente completo
uv run python labs/03-mcp/chatbot.py --local --debug       # solo tools locales
```

Comandos del chatbot: `/tools`, `/recursos`, `/leer academico://calendario`, `/reiniciar`, `/salir`.

Para el Paso 0 (asistente del Lab 02): `uv run python labs/02-rag/ingest.py` y luego
`uv run python labs/02-rag/chatbot.py`.

## Reproducir todas las evidencias

```bash
uv run python labs/02-rag/ingest.py
uv run python scripts/generar_evidencias.py           # todo
uv run python scripts/generar_evidencias.py t8 e4     # solo algunos casos
```

Genera en `evidencias/` la salida de los Pasos 0, 2, 6, 7 y 8 y de las pruebas 1 a 10.
Los estados "antes del TODO" se simulan en memoria con `scripts/parches.py`, sin modificar el código.

## Estructura

```text
labs/03-mcp/
├── chatbot.py       interfaz CLI: arranca el servidor MCP, confirma acciones, --debug
├── assistant.py     ciclo pedir → ejecutar → responder y confirmación de acciones
├── llm_client.py    único módulo que conoce al proveedor (envía tools, devuelve tool_calls)
├── tools.py         clase Tool y tools locales (fecha_actual, calcular_nota_final)
├── tool_calling.py  tool calling sin ejecución
├── mcp_server.py    servidor MCP "servicios-academicos" (tools + resource del calendario)
├── mcp_client.py    adaptador: tools MCP → Tool
├── prompts.py       prompt de sistema con reglas de uso de tools
├── config.py        configuración desde .env
└── data/academico.json
labs/02-rag/         asistente RAG del Lab 02 (Paso 0)
scripts/             generación de evidencias
```
