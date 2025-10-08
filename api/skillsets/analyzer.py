# /api/skillsets/analyzer.py
# Skillset de Análisis de Código con g4f, optimizado para Vercel.

import g4f
import asyncio

# --- Configuración de g4f ---
g4f.debug.logging = False
g4f.debug.check_version = False

class Analyzer:
    """
    Un Skillset que analiza código actuando como un colaborador experto,
    utilizando g4f con un proveedor específico para mayor estabilidad.
    """
    
    async def ejecutar(self, datos_peticion):
        """
        El método principal que el motor A.L.E. llamará.
        """
        print("-> Iniciando diálogo con el Skillset 'Analyzer' (Motor: g4f)...")
        
        codigo_a_analizar = datos_peticion.get("codigo")
        if not codigo_a_analizar:
            print("   Error: No se encontró 'codigo' en la petición.")
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
            print("   Enviando código a g4f (Proveedor: GptGo) para análisis...")
            
            # --- LLAMADA A G4F CORREGIDA ---
            # Forzamos el uso de un proveedor que es conocido por ser más estable en entornos de servidor.
            respuesta_ia = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": codigo_a_analizar}
                ],
                provider=g4f.Provider.GptGo, # <-- La línea clave para la estabilidad
                timeout=300 
            )
            
            print("   Análisis recibido de g4f.")
            # Devolvemos un JSON con el análisis, que es lo que el frontend espera.
            return {"analisis": respuesta_ia}

        except Exception as e:
            error_msg = f"Hubo un problema al dialogar con el motor g4f. El proveedor puede estar sobrecargado. Detalles: {str(e)}"
            print(f"   🚨 {error_msg}")
            # Devolvemos un JSON de error, para que el frontend no se rompa y muestre un mensaje claro.
            return {"error": error_msg}
