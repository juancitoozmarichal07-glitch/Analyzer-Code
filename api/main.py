# /api/main.py
# VERSIÓN FINAL para g4f actualizado en Vercel

import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

# --- 1. CONFIGURACIÓN DEL SERVIDOR FLASK ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
print("✅ Servidor Flask inicializado.")

# --- 2. LÓGICA DEL ANALIZADOR (adaptada para g4f moderno) ---
async def analizar_codigo(codigo_a_analizar):
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
        print("   Enviando código a g4f (versión actualizada, proveedor automático) para análisis...")
        
        # Sintaxis para las versiones más nuevas de g4f
        respuesta_ia = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": codigo_a_analizar}
            ]
        )
        
        print("   Análisis recibido de g4f.")
        return {"analisis": respuesta_ia}

    except Exception as e:
        error_msg = f"Hubo un problema con el motor g4f actualizado. Detalles: {str(e)}"
        print(f"   🚨 {error_msg}")
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

# --- 3. RUTA DE LA API ---
@app.route('/api/execute', methods=['POST'])
def handle_execution():
    codigo = request.json.get("codigo")
    if not codigo:
        return jsonify({"error": "No se proporcionó código."}), 400
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    resultado = loop.run_until_complete(analizar_codigo(codigo))
    return jsonify(resultado)
