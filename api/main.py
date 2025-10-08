# backend/main.py (Versión Final API-Only para Vercel)

import sys
import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Configuración de la App Flask ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) # CORS solo para la ruta de la API

# --- Bloque de Rutas para Vercel ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- Importaciones Esenciales ---
from ale_core import ALE_Core
from skillsets.analyzer import Analyzer

# --- Inicialización del Motor A.L.E. ---
ale = ALE_Core()
ale.cargar_skillset("analyzer", Analyzer())

print("✅ Backend de A.L.E. listo para recibir peticiones en /api/execute.")

# --- Ruta de la API ---
# Esta es la ÚNICA ruta que manejará nuestro backend de Python.
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

# NO hay ruta para '/', Flask ya no se encarga del frontend.
