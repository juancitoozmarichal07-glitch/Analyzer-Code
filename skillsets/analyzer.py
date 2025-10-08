# /skillsets/analyzer.py
# Skillset de Análisis de Código. Actúa como un colaborador experto.

import g4f
import asyncio

# Versión de g4f que estamos usando: 0.6.3.4
# No es necesario configurar nada más si ya está instalado.
# g4f.debug.logging = False # Mantenlo comentado a menos que necesites depurar.

class Analyzer:
    """
    Un Skillset para A.L.E. que analiza código actuando como un
    programador senior colaborador, no como un juez.
    Utiliza g4f para acceder a modelos de lenguaje potentes.
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

        # --- PROMPT DEL SISTEMA ACTUALIZADO ---
        # Este prompt instruye a la IA para que adopte un tono de colaborador.
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
            print("   Enviando código al motor de IA para obtener su perspectiva...")
            
            # Llamada asíncrona a g4f
            respuesta_ia = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4, # Modelo potente para análisis de alta calidad
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": codigo_a_analizar}
                ],
                timeout=300 # Tiempo de espera de 5 minutos para análisis complejos
            )
            
            print("   Perspectiva del análisis recibida.")
            return {"analisis": respuesta_ia}

        except Exception as e:
            # Captura de errores de conexión o de la librería g4f
            error_msg = f"Hubo un problema al dialogar con el motor de IA. Puede estar sobrecargado o sin conexión. Revisa tu conexión a internet. Detalles: {str(e)}"
            print(f"   🚨 {error_msg}")
            import traceback
            traceback.print_exc()
            return {"error": error_msg}

