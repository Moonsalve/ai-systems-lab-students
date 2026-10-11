"""Ejecuta un script de los labs, opcionalmente simulando el estado "antes del TODO" (Pasos 2, 6, 7 y 8.2).

No modifica el código del lab: aplica los cambios en memoria y luego ejecuta el script.

Uso (desde la raíz del repositorio):
    uv run python scripts/parches.py [--sin-todo1] [--sin-todo5] [--prompt-original] [--desc-fecha] \
        labs/03-mcp/<script>.py [argumentos del script...]
"""

import runpy
import sys
from pathlib import Path

PARCHES = {"--sin-todo1", "--sin-todo5", "--prompt-original", "--desc-fecha"}

PROMPT_ORIGINAL = """Eres el Asistente Inteligente del Curso de Inteligencia Artificial \
de Ingeniería de Sistemas e Ingeniería de Software.

Reglas:
- Responde en español, de forma clara y concisa (máximo un párrafo, salvo que pidan más detalle).
- Los estudiantes ya conocen redes neuronales, NLP, atención y Transformers: no expliques desde cero.
- Si la pregunta no está relacionada con IA o con el curso, indícalo amablemente."""

DESC_EXPERIMENTO = "Devuelve la fecha en que se creó el curso. No sirve para conocer la fecha de hoy."


def eco_de_entradas() -> None:
    """Con la entrada redirigida (no interactiva), muestra lo que se "escribió" para que la
    transcripción se lea como una sesión real."""
    if sys.stdin.isatty():
        return
    import builtins

    input_original = builtins.input

    def input_con_eco(prompt: str = "") -> str:
        linea = input_original(prompt)
        print(linea, flush=True)
        return linea

    builtins.input = input_con_eco


def main() -> None:
    args = sys.argv[1:]
    activos = {a for a in args if a in PARCHES}
    resto = [a for a in args if a not in PARCHES]
    script = Path(resto[0]).resolve()
    sys.path.insert(0, str(script.parent))
    eco_de_entradas()

    if activos:
        import assistant
        import prompts
        import tools

        if "--sin-todo1" in activos:  # calcular_nota_final sin argumentos declarados
            tools.LOCAL_TOOLS[1].parameters = {"type": "object", "properties": {}, "required": []}
        if "--desc-fecha" in activos:  # Paso 8.2: misma función, otra descripción
            tools.LOCAL_TOOLS[0].description = DESC_EXPERIMENTO
        if "--prompt-original" in activos:  # Paso 7: prompt sin la sección de tools
            prompts.SYSTEM_PROMPT = PROMPT_ORIGINAL
        if "--sin-todo5" in activos:  # Paso 6: nadie pide confirmación
            original_init = assistant.CourseAssistant.__init__

            async def siempre_si(tool, arguments):
                return True

            def init_sin_confirmacion(self, llm, tool_list, confirm):
                original_init(self, llm, tool_list, siempre_si)

            assistant.CourseAssistant.__init__ = init_sin_confirmacion

    if activos:
        print(f"[parches activos: {', '.join(sorted(activos))}]")
    sys.argv = [str(script), *resto[1:]]
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
