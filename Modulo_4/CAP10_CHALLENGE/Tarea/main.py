from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.schema import SystemMessage
import pandas as pd
import re

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

class BankingAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.1)
        
        # Configuración de embeddings y base de conocimientos
        embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        
        self.db = FAISS.load_local(
            "./solution/index",
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        self.retriever = self.db.as_retriever(k=3)
        
        # Cargar datos de balances
        self.balances_df = pd.read_csv("./saldos.csv")
        
        # Definir herramientas
        self.tools = [self.get_balance_by_id, self.get_bank_information]
        
        # Crear agente
        self.agent = create_react_agent(self.llm, self.tools, prompt=hub.pull("hwchase17/react"))
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True
        )
    
    @tool
    def get_balance_by_id(self, cedula_id: str) -> str:
        """Obtiene balance de la cuenta by cedula_id. El ID debe estar en formato V-12345678"""
        try:
            # Normalizar el formato del ID
            cedula_id = cedula_id.upper().strip()
            if not cedula_id.startswith('V-'):
                cedula_id = f"V-{cedula_id}"
            
            result = self.balances_df[self.balances_df["ID_Cedula"] == cedula_id]
            
            if len(result) == 0:
                return f"No se encontró ninguna cuenta con el ID: {cedula_id}"
            
            balance = result["Balance"].values[0]
            return f"El balance de la cuenta con ID {cedula_id} es: ${balance:,.2f}"
        
        except Exception as e:
            return f"Error al consultar el balance: {str(e)}"
    
    @tool
    def get_bank_information(self, question: str) -> str:
        """Obtiene información específica del banco sobre trámites, productos y servicios bancarios"""
        try:
            bank_info_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                verbose=False,
            )
            response = bank_info_chain.run({
                "query": question,
                "context": "Eres un asistente bancario especializado en información sobre cuentas de ahorros, tarjetas de crédito, transferencias y trámites bancarios."
            })
            return response
        except Exception as e:
            return f"Error al consultar la información bancaria: {str(e)}"
    
    def classify_query(self, query: str) -> str:
        """Clasifica la consulta para determinar el flujo apropiado"""
        query_lower = query.lower()
        
        # Patrones para consultas de balance
        balance_patterns = [
            r'balance.*cedula.*v-?\d+',
            r'saldo.*cedula.*v-?\d+',
            r'v-?\d+.*balance',
            r'v-?\d+.*saldo',
            r'cuanto.*tengo.*cuenta',
            r'mi.*balance',
            r'mi.*saldo'
        ]
        
        # Patrones para consultas bancarias específicas
        bank_patterns = [
            r'abrir.*cuenta',
            r'tarjeta.*credito',
            r'transferencia',
            r'tramite',
            r'requisito',
            r'proceso',
            r'banco.*como',
            r'que.*necesito.*para',
            r'como.*funciona'
        ]
        
        # Verificar si es consulta de balance
        for pattern in balance_patterns:
            if re.search(pattern, query_lower):
                return "balance"
        
        # Verificar si es consulta bancaria específica
        for pattern in bank_patterns:
            if re.search(pattern, query_lower):
                return "bank_info"
        
        # Por defecto, consulta general
        return "general"
    
    def process_query(self, query: str) -> str:
        """Procesa la consulta y decide el método de respuesta apropiado"""
        query_type = self.classify_query(query)
        
        print(f"Tipo de consulta detectado: {query_type}")
        
        if query_type == "balance":
            # Extraer ID de cédula si está presente
            cedula_match = re.search(r'v-?\d+', query.lower())
            if cedula_match:
                cedula_id = cedula_match.group(0)
                return self.get_balance_by_id(cedula_id)
            else:
                return "Para consultar su balance, por favor proporcione su número de cédula en formato V-12345678"
        
        elif query_type == "bank_info":
            return self.get_bank_information(query)
        
        else:
            # Consulta general - usar el LLM directamente
            try:
                response = self.llm.invoke([
                    SystemMessage(content="Eres un asistente bancario útil y profesional. Responde preguntas generales de manera clara y concisa."),
                    {"role": "user", "content": query}
                ])
                return response.content
            except Exception as e:
                return f"Error al procesar la consulta: {str(e)}"

# Función principal para probar el sistema
def main():
    assistant = BankingAssistant()
    
    # Ejemplos de consultas para probar los diferentes flujos
    test_queries = [
        "Hola, ¿cómo estás?",
        "¿Cómo abro una cuenta de ahorros en el banco?",
        "¿Cuál es el balance de la cuenta de la cédula V-91827364?",
        "Necesito saber mi saldo con cédula V-12345678",
        "¿Cómo puedo obtener una tarjeta de crédito?",
        "¿Cuáles son los requisitos para hacer una transferencia internacional?",
        "¿Cuál es el sentido de la vida?",
        "¿Qué tiempo hará mañana?"
    ]
    
    print("=== Sistema de Asistente Bancario ===")
    print("Probando diferentes tipos de consultas:\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Consulta {i}: '{query}' ---")
        response = assistant.process_query(query)
        print(f"Respuesta: {response}")
        print("-" * 80)

if __name__ == "__main__":
    main()