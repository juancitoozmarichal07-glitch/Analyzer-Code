# /api/main.py
# Versión "Todo en Uno" con g4f, robusta para Vercel.

import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

# --- 1. CONFIGURACIÓN DE g4f ---
g4f.debug.logging = False
g4f.debug.check_version = False
print("✅ Motor de IA (g4f) configurado.")

# --- 2. CONFIGURACIÓN DEL SERVIDOR FLASK ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
print("✅ Servidor Flask inicializado.")

# --- 3. LÓGICA DEL ANALIZADOR (integrada con g4f) ---
async def analizar_codigo(codigo_a_analizar):
    """
    Función asíncrona que llama a g4f para analizar el código.
    """
    prompt_sistema = """
    Eres un programador senior experto, actuando como un colaborador y mentor. Tu tono es constructivo y respetuoso. Tu misión es analizar el código y devolver un informe estructurado.
    Responde ÚNICA Y EXCLUSIVAMENTE con la siguiente estructura:
    [LENGUAJE IDENTIFICADO]: ...
    [QUÉ ES]: ...
    [PARA QUÉ SIRVE]: ...
    [ANÁLISIS DE ERRORES Y MEJORAS]: ...
    [SOLUCIONES PROPUESTAS]: ...
    [POSIBLES EXTENSIONES]: ...
    """

    try:
        print("   Enviando código a g4f (Proveedor: GptGo) para análisis...")
        
        # Llamada a g4f forzando un proveedor estable
        respuesta_ia = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": codigo_a_analizar}
            ],
            provider=g4f.Provider.GptGo, # Forzamos un proveedor fiable
            timeout=300
        )
        
        print("   Análisis recibido de g4f.")
        return {"analisis": respuesta_ia}

    except Exception as e:
        error_msg = f"Hubo un problema al dialogar con el motor g4f. El proveedor puede estar sobrecargado. Detalles: {str(e)}"
        print(f"   🚨 {error_msg}")
        # Devolvemos un JSON de error, para que el frontend no se rompa.
        return {"error": error_msg}

# --- 4. RUTA DE LA API ---
@app.route('/api/execute', methods=['POST'])
def handle_execution():
    datos_peticion = request.json
    codigo = datos_peticion.get("codigo")

    if not codigo:
        return jsonify({"error": "No se proporcionó código en la petición."}), 400

    # Lógica para ejecutar la función asíncrona desde Flask
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    resultado = loop.run_until_complete(analizar_codigo(codigo))
    
    return jsonify(resultado)
