# backend/main.py (Versión Final y Limpia para Vercel)

import sys
import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuración de la App Flask ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Bloque de Rutas para Vercel ---
# Añade la ruta del directorio actual al path de Python para encontrar ale_core
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- Importaciones Esenciales ---
# Solo importamos lo que realmente existe en nuestro repositorio
from ale_core import ALE_Core
from skillsets.analyzer import Analyzer

# --- Inicialización del Motor A.L.E. ---
ale = ALE_Core()

print("Cargando skillset 'Analyzer' en el motor A.L.E...")
ale.cargar_skillset("analyzer", Analyzer()) # Solo cargamos el skillset que tenemos

print("✅ Servidor listo. A.L.E. está online con el skillset 'Analyzer'.")

# --- Ruta de la API ---
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

# --- Ruta para la Raíz (Sirve el index.html) ---
@app.route('/', methods=['GET'])
def serve_index():
    # Esto le dice a Flask que envíe el archivo index.html cuando alguien visita la URL principal
    return app.send_static_file('index.html')

# Vercel usará la variable 'app' para ejecutar el servidor.
# El bloque if __name__ == "__main__": es ignorado en producción.
