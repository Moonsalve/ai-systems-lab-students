"""Ejecuta los pasos, las diez pruebas y los experimentos del Lab 03 y guarda cada salida en evidencias/.

Requiere un .env con un modelo que soporte tool calling y, para el Paso 0, el índice
del Lab 02 (uv run python labs/02-rag/ingest.py). Ninguna salida incluye la API key.

Uso (funciona desde cualquier carpeta; se recomienda la raíz del repositorio):
    uv run python scripts/generar_evidencias.py            # todo
    uv run python scripts/generar_evidencias.py p2 t8      # solo algunos casos
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # raíz del repositorio
OUT = ROOT / "evidencias"


def interprete() -> str:
    """El Python del entorno de uv (.venv), aunque el script se lance con otro Python."""
    for candidato in (ROOT / ".venv" / "Scripts" / "python.exe", ROOT / ".venv" / "bin" / "python"):
        if candidato.exists():
            return str(candidato)
    return sys.executable


PY = interprete()
L3 = "labs/03-mcp"
NOTAS = "Si saco 4 en los parciales, 3.5 en laboratorios y 4.2 en el proyecto, ¿apruebo?"
SUP_3 = "Mi código es 2026003. No fui al primer parcial por incapacidad médica: solicita el supletorio."
SUP_2 = "Mi código es 2026002. No fui al primer parcial por incapacidad médica: solicita el supletorio."

# (id, archivo, comando, líneas que se escriben en la consola)
CASOS = [
    # Paso 0: el asistente del Lab 02 frente a preguntas que requieren tools
    ("p0", "paso0_lab02.txt", [PY, "labs/02-rag/chatbot.py"], [
        "¿Qué día es hoy?", "/reiniciar",
        "¿Cuáles son mis notas? Mi código es 2026001", "/reiniciar",
        "No pude ir al primer parcial por incapacidad médica, mi código es 2026003. Solicita el supletorio.",
        "/salir"]),
    ("p0b", "paso0_lab03.txt", [PY, f"{L3}/chatbot.py"], [
        "¿Qué día es hoy?", "/reiniciar",
        "¿Cuáles son mis notas? Mi código es 2026001", "/reiniciar",
        "No pude ir al primer parcial por incapacidad médica, mi código es 2026003. Solicita el supletorio.",
        "s", "/salir"]),
    # Prueba 1
    ("t1", "prueba01_tools.txt", [PY, f"{L3}/tools.py"], []),
    # Paso 2 / Pruebas 2 y 3
    ("t2", "prueba02_fecha.txt", [PY, f"{L3}/tool_calling.py", "¿Qué día es hoy?"], []),
    ("p2a", "paso2_notas_antes_todo1.txt", [PY, "scripts/parches.py", "--sin-todo1", f"{L3}/tool_calling.py", NOTAS], []),
    ("t3", "prueba03_notas_despues_todo1.txt", [PY, f"{L3}/tool_calling.py", NOTAS], []),
    ("p2c", "paso2_transformer.txt", [PY, f"{L3}/tool_calling.py", "¿Qué es la atención en un Transformer?"], []),
    # Paso 3 / Prueba 4
    ("t4", "prueba04_ciclo_local_debug.txt", [PY, f"{L3}/chatbot.py", "--local", "--debug"], [
        "¿Qué día es hoy?", "/reiniciar", NOTAS, "/salir"]),
    # Prueba 5
    ("t5", "prueba05_cliente_mcp.txt", [PY, f"{L3}/mcp_client.py"], []),
    # Paso 6 antes del TODO 5
    ("p6a", "paso6_supletorio_sin_confirmacion.txt", [PY, "scripts/parches.py", "--sin-todo5", f"{L3}/chatbot.py", "--debug"], [
        "/tools", SUP_3, "/salir"]),
    # Pruebas 6 y 7
    ("t6", "prueba06_notas_mcp.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "¿Cuáles son mis notas? Mi código es 2026001", "/salir"]),
    ("t7", "prueba07_error_9999.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "Consulta las notas del estudiante 9999", "/salir"]),
    # Pruebas 8 y 9 (misma sesión: el servidor guarda las solicitudes en memoria)
    ("t8", "prueba08_09_confirmacion_debug.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "/tools", SUP_3, "s", "/reiniciar", SUP_2, "n", "/reiniciar",
        "¿Qué solicitudes tengo? código 2026003", "/salir"]),
    # Prueba 10 y Paso 8.1
    ("t10", "prueba10_resource.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "/recursos", "/leer academico://calendario", "/salir"]),
    # Paso 7: antes y después del TODO 6
    ("p7a", "paso7_antes_todo6.txt", [PY, "scripts/parches.py", "--prompt-original", f"{L3}/chatbot.py", "--debug"], [
        "¿Cuáles son mis notas?", "/reiniciar",
        "¿Cuánto es 0.2·4 + 0.2·3.5 + 0.35·4.2 + 0.25·3.8?", "/reiniciar",
        "Consulta las notas del estudiante 9999", "/salir"]),
    ("p7b", "paso7_despues_todo6.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "¿Cuáles son mis notas?", "/reiniciar",
        "¿Cuánto es 0.2·4 + 0.2·3.5 + 0.35·4.2 + 0.25·3.8?", "/reiniciar",
        "Consulta las notas del estudiante 9999", "/salir"]),
    # Paso 8: experimentos
    ("e2", "paso8_2_descripcion.txt", [PY, "scripts/parches.py", "--desc-fecha", f"{L3}/chatbot.py", "--local", "--debug"], [
        "¿Qué día es hoy?", "/salir"]),
    ("e3a", "paso8_3_tokens_local.txt", [PY, f"{L3}/chatbot.py", "--local", "--debug"], ["hola", "/salir"]),
    ("e3b", "paso8_3_tokens_mcp.txt", [PY, f"{L3}/chatbot.py", "--debug"], ["hola", "/salir"]),
    ("e4", "paso8_4_limite.txt", [PY, f"{L3}/chatbot.py", "--debug"], [
        "Mi código es 2026001. Si saco 4.0 en los dos parciales y 4.0 en el proyecto, ¿con cuánto quedo?",
        "/salir"]),
]


def main() -> None:
    elegidos = set(sys.argv[1:])
    OUT.mkdir(exist_ok=True)
    for caso_id, archivo, comando, entradas in CASOS:
        if elegidos and caso_id not in elegidos:
            continue
        print(f"→ {caso_id}: {archivo}")
        stdin = "\n".join(entradas) + "\n" if entradas else ""
        if comando[1] != "scripts/parches.py":
            comando = [PY, "scripts/parches.py", *comando[1:]]  # sin parches: solo eco de entradas
        # En Windows la consola redirigida usa cp1252 y falla con caracteres como "→": forzamos UTF-8.
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        proc = subprocess.run(
            comando, input=stdin, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=600, env=env, cwd=ROOT,
        )
        args = [c for c in comando[2:] if not c.startswith("--sin-") and c not in ("--prompt-original", "--desc-fecha")]
        parches = [c for c in comando[2:] if c not in args]
        cabecera = "$ uv run python " + " ".join(f'"{c}"' if " " in c else c for c in args) + "\n"
        if parches:
            cabecera += f"# Estado simulado con scripts/parches.py: {' '.join(parches)}\n"
        if entradas:
            cabecera += "# Entradas escritas en la consola, en orden:\n" + "".join(f"#   {e}\n" for e in entradas)
        texto = cabecera + "\n" + proc.stdout
        if proc.stderr.strip():
            texto += "\n[stderr]\n" + proc.stderr
        (OUT / archivo).write_text(texto, encoding="utf-8")
        time.sleep(3)  # margen para los límites de peticiones por minuto del plan gratuito
    print(f"\nListo. Revisa las salidas en {OUT}")


if __name__ == "__main__":
    main()
