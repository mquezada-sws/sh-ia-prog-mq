import os
import requests
import json
import time
from typing import List, Dict, Any, Generator
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Chatbot:
    def __init__(self):
        # Configurar API keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        
        if not self.openai_api_key or not self.serper_api_key:
            raise ValueError("API keys no encontradas. Verifica tu archivo .env")
        
        openai.api_key = self.openai_api_key
        
        # Memoria de la conversación
        self.conversation_history: List[Dict[str, str]] = []
        
        # Configuración inicial del sistema
        self.system_prompt = """Eres un asistente inteligente y útil. 
        Cuando sea necesario, puedes realizar búsquedas en internet para obtener información actualizada.
        Siempre cita tus fuentes cuando uses información de búsquedas.
        Responde de manera clara y concisa."""
        
        self.conversation_history.append({"role": "system", "content": self.system_prompt})
    
    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Realiza una búsqueda web usando Serper.dev
        """
        try:
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": query,
                "num": 5  # Número de resultados
            })
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extraer información relevante de los resultados
            search_results = []
            
            # Resultados orgánicos
            if 'organic' in data:
                for result in data['organic']:
                    search_results.append({
                        'title': result.get('title', ''),
                        'link': result.get('link', ''),
                        'snippet': result.get('snippet', '')
                    })
            
            # Respuestas directas (featured snippets)
            if 'answerBox' in data:
                answer_box = data['answerBox']
                search_results.insert(0, {
                    'title': answer_box.get('title', 'Direct Answer'),
                    'link': answer_box.get('link', ''),
                    'snippet': answer_box.get('answer', '') or answer_box.get('snippet', '')
                })
            
            return search_results
            
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []
    
    def should_search(self, user_input: str) -> bool:
        """
        Determina si es necesario realizar una búsqueda basado en la entrada del usuario
        """
        # Palabras clave que indican necesidad de búsqueda
        search_keywords = [
            'actual', 'reciente', '202', 'noticia', 'último', 'buscar', 
            'en internet', 'online', 'web', 'noticias', 'tendencias',
            'estadísticas', 'datos actuales', 'información reciente'
        ]
        
        # Preguntas sobre información que puede cambiar
        question_words = ['qué', 'cuándo', 'dónde', 'cómo', 'por qué', 'quién', 'cuál']
        
        user_input_lower = user_input.lower()
        
        # Si contiene palabras clave de búsqueda
        if any(keyword in user_input_lower for keyword in search_keywords):
            return True
        
        # Si es una pregunta sobre información potencialmente cambiante
        if any(user_input_lower.startswith(word) for word in question_words):
            return True
        
        return False
    
    def format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formatea los resultados de búsqueda para incluirlos en el contexto
        """
        if not results:
            return "No se encontraron resultados relevantes en la búsqueda."
        
        formatted = "Resultados de búsqueda:\n\n"
        for i, result in enumerate(results[:3], 1):  # Limitar a 3 resultados
            formatted += f"[Fuente {i}]: {result['title']}\n"
            formatted += f"URL: {result['link']}\n"
            formatted += f"Información: {result['snippet']}\n\n"
        
        return formatted
    
    def generate_response_stream(self, user_input: str) -> Generator[str, None, None]:
        """
        Genera una respuesta en streaming usando OpenAI
        """
        # Añadir mensaje del usuario al historial
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Determinar si se necesita búsqueda
        search_query = None
        search_results = None
        
        if self.should_search(user_input):
            # Extraer términos de búsqueda relevantes
            search_query = user_input
            search_results = self.search_web(search_query)
            
            if search_results:
                search_context = self.format_search_results(search_results)
                # Añadir contexto de búsqueda al historial temporal
                temp_history = self.conversation_history.copy()
                temp_history.append({
                    "role": "system", 
                    "content": f"Información obtenida de búsqueda web:\n{search_context}\n\nResponde usando esta información cuando sea relevante y cita las fuentes."
                })
            else:
                temp_history = self.conversation_history
        else:
            temp_history = self.conversation_history
        
        try:
            # Realizar llamada a OpenAI con streaming
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=temp_history,
                stream=True,
                max_tokens=1000,
                temperature=0.7
            )
            
            full_response = ""
            
            # Procesar stream de respuesta
            for chunk in response:
                if 'content' in chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                        full_response += content
                        time.sleep(0.01)  # Pequeña pausa para efecto de streaming
            
            # Añadir respuesta completa al historial
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # Mostrar fuentes si se realizó búsqueda
            if search_results and search_query:
                yield "\n\n🔍 **Fuentes consultadas:**\n"
                for i, result in enumerate(search_results[:3], 1):
                    yield f"{i}. [{result['title']}]({result['link']})\n"
                    
        except Exception as e:
            error_msg = f"❌ Error al generar respuesta: {str(e)}"
            yield error_msg
            self.conversation_history.append({"role": "assistant", "content": error_msg})
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
    
    def show_history(self):
        """Muestra el historial de conversación"""
        print("\n" + "="*50)
        print("HISTORIAL DE CONVERSACIÓN")
        print("="*50)
        for msg in self.conversation_history:
            if msg['role'] == 'system':
                continue  # Omitir prompt del sistema
            role = "Usuario" if msg['role'] == 'user' else "Asistente"
            print(f"\n{role}: {msg['content']}")
        print("="*50 + "\n")

def main():
    """Función principal para ejecutar el chatbot en consola"""
    try:
        chatbot = Chatbot()
        print("🤖 Chatbot iniciado. Escribe 'salir' para terminar, 'limpiar' para borrar historial, 'historial' para ver conversación.")
        print("-" * 80)
        
        while True:
            try:
                user_input = input("\n👤 Tú: ").strip()
                
                if user_input.lower() == 'salir':
                    print("👋 ¡Hasta luego!")
                    break
                elif user_input.lower() == 'limpiar':
                    chatbot.clear_history()
                    print("🗑️ Historial limpiado.")
                    continue
                elif user_input.lower() == 'historial':
                    chatbot.show_history()
                    continue
                elif not user_input:
                    continue
                
                print("\n🤖 Asistente: ", end="", flush=True)
                
                # Generar y mostrar respuesta en streaming
                for chunk in chatbot.generate_response_stream(user_input):
                    print(chunk, end="", flush=True)
                
                print()  # Nueva línea después de la respuesta
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupción detectada. Escribe 'salir' para terminar.")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                
    except ValueError as e:
        print(f"Error de configuración: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()