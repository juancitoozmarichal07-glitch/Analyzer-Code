# backend/main.py (Versión Robusta para Vercel)

import sys
import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuración de la App Flask ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Bloque de Rutas Modificado para Vercel ---
# Esto asegura que Python encuentre la carpeta 'skillsets' sin importar cómo lo ejecute Vercel.
# Obtenemos la ruta del directorio donde se encuentra main.py
basedir = os.path.abspath(os.path.dirname(__file__))
# Añadimos la carpeta 'skillsets' que está dentro de ese directorio al path de Python
sys.path.insert(0, os.path.join(basedir, 'skillsets'))
# -------------------------------------------------

# --- Importación de los Skillsets Esenciales ---
# Ahora estas importaciones funcionarán de forma fiable en Vercel
from ale_core import ALE_Core
from analyzer import Analyzer

# --- Inicialización del Motor A.L.E. ---
ale = ALE_Core()

print("Cargando skillsets en el motor A.L.E...")
ale.cargar_skillset("analyzer", Analyzer())

print("✅ Servidor listo. A.L.E. está online.")

# --- Ruta de la API ---
# El resto del código no necesita cambios.
@app.route('/api/execute', methods=['POST'])
def handle_execution():
    datos_peticion = request.json
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    respuesta_de_ale = loop.run_until_complete(ale.procesar_peticion(datos_peticion))
    return jsonify(respuesta_de_ale)

# --- Arranque del Servidor ---
# Esta parte es principalmente para desarrollo local, Vercel usa la 'app' directamente.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

