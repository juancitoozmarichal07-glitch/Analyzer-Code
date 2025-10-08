# /api/skillsets/analyzer.py
# Skillset de Análisis de Código. Actúa como un colaborador experto.
# Versión corregida para funcionar de forma estable en Vercel.

import g4f
import asyncio

# --- Configuración de g4f ---
# Es una buena práctica deshabilitar logs innecesarios en producción.
g4f.debug.logging = False
g4f.debug.check_version = False

class Analyzer:
    """
    Un Skillset para A.L.E. que analiza código actuando como un
    programador senior colaborador. Utiliza g4f con un proveedor
    específico para mayor estabilidad en entornos de nube como Vercel.
    """
    
    async def ejecutar(self, datos_peticion):
        """
        El método principal que el motor A.L.E. llamará.
        Recibe el código y devuelve un análisis colaborativo.
        """
        print("-> Iniciando diálogo con el Skillset 'Analyzer'...")
        
        codigo_a_analizar = datos_peticion.get("codigo")
        if not codigo_a_analizar:
            print("   Error: No se encontró 'codigo' en la petición.")
            return {"error": "Petición inválida: Debes incluir el campo 'codigo' para iniciar el análisis."}

        # --- PROMPT DEL SISTEMA ---
        # Instruye a la IA para que adopte un tono de colaborador.
        prompt_sistema = """
        Eres un programador senior experto, actuando como un colaborador y mentor.
        Tu tono es constructivo y respetuoso, nunca autoritario.
        Tu misión es analizar el código que te proporciona el usuario y devolver un informe estructurado que sirva como punto de partida para un diálogo técnico.
        
        Responde ÚNICA Y EXCLUSIVAMENTE con la siguiente estructura:

        [LENGUAJE IDENTIFICADO]: Tu mejor suposición del lenguaje de programación.
        
        [QUÉ ES]: Describe técnicamente la funcionalidad y arquitectura del código.
        
        [PARA QUÉ SIRVE]: Explica en lenguaje sencillo el propósito y la utilidad del código, como si se lo explicaras a un colega.
        
        [ANÁLISIS DE ERRORES Y MEJORAS]: Presenta una lista numerada de observaciones. Enfócate en debilidades estructurales, riesgos potenciales y oportunidades de mejora (robustez, legibilidad, eficiencia). Usa un lenguaje como "Se podría considerar...", "Un área de mejora podría ser...", "Un riesgo potencial aquí es...".
        
        [SOLUCIONES PROPUESTAS]: Ofrece fragmentos de código como ejemplos concretos para las mejoras sugeridas. Preséntalos como "Una posible implementación podría ser así:".
        
        [POSIBLES EXTENSIONES]: Sugiere 2 o 3 ideas para evolucionar el proyecto, presentándolas como "¿Has considerado explorar...?".
        """

        try:
            print("   Enviando código al motor de IA (Proveedor: GptGo) para obtener su perspectiva...")
            
            # --- LLAMADA A G4F CORREGIDA ---
            # Forzamos el uso de un proveedor que es conocido por ser más estable en entornos de servidor.
            # Este es el cambio clave para evitar el error anterior.
            respuesta_ia = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": codigo_a_analizar}
                ],
                provider=g4f.Provider.GptGo, # <-- ¡LA LÍNEA MÁGICA!
                timeout=300 
            )
            
            print("   Perspectiva del análisis recibida correctamente.")
            return {"analisis": respuesta_ia}

        except Exception as e:
            # Captura de errores de conexión o de la librería g4f
            error_msg = f"Hubo un problema al dialogar con el motor de IA. El proveedor puede estar sobrecargado. Por favor, inténtalo de nuevo. Detalles: {str(e)}"
            print(f"   🚨 {error_msg}")
            import traceback
            traceback.print_exc()
            return {"error": error_msg}

