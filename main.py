# backend/main.py (Tu código + Analyzer integrado)
import sys
import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuración de la App Flask ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Importación de los Skillsets Esenciales ---
from ale_core import ALE_Core
from skillsets.guardian import Guardian
from skillsets.oracle import Oracle
from skillsets.veridian import Veridian
from skillsets.akinator import Akinator
from skillsets.analyzer import Analyzer  # <-- 1. AÑADIMOS LA IMPORTACIÓN DEL ANALYZER

# --- Inicialización del Motor A.L.E. ---
ale = ALE_Core()

print("Cargando skillsets esenciales en el motor A.L.E...")
ale.cargar_skillset("guardian", Guardian())
ale.cargar_skillset("oracle", Oracle())
ale.cargar_skillset("veridian", Veridian())
ale.cargar_skillset("akinator", Akinator())
ale.cargar_skillset("analyzer", Analyzer()) # <-- 2. CARGAMOS EL SKILLSET EN EL MOTOR

# Hemos actualizado el mensaje para reflejar que el Analyzer está listo
print("✅ Servidor listo. A.L.E. está online con todos los skillsets, incluido el Analyzer.") # <-- 3. (Opcional) MENSAJE ACTUALIZADO

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

# --- Arranque del Servidor ---
if __name__ == "__main__":
    # Añadimos un mensaje de inicio para mayor claridad
    print("Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
