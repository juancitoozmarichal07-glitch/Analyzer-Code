# /api/skillsets/analyzer.py
# VERSIÓN FINAL para g4f actualizado en Vercel, con proveedor automático.

import g4f
import asyncio

# --- Configuración de g4f ---
# No es necesario tocar esto.
g4f.debug.logging = False
g4f.debug.check_version = False

class Analyzer:
    """
    Un Skillset que analiza código usando la versión más reciente de g4f.
    """
    
    async def ejecutar(self, datos_peticion):
        """
        El método principal que el motor A.L.E. llamará.
        """
        print("-> Iniciando diálogo con el Skillset 'Analyzer' (Motor: g4f actualizado)...")
        
        codigo_a_analizar = datos_peticion.get("codigo")
        if not codigo_a_analizar:
            return {"error": "Petición inválida: Debes incluir el campo 'codigo'."}

        # --- PROMPT DEL SISTEMA ---
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
            print("   Enviando código a g4f (proveedor automático) para análisis...")
            
            # --- LLAMADA A G4F ADAPTADA ---
            # Esta sintaxis es para las versiones más nuevas de g4f.
            # No especificamos 'provider' para dejar que la librería elija el mejor.
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
