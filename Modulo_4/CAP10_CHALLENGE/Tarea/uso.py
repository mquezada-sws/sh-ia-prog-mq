
from Tarea.main import BankingAssistant

assistant = BankingAssistant()

# Procesar consultas
response = assistant.process_query("¿Cuál es mi saldo con cédula V-91827364?")
print(response)

response = assistant.process_query("¿Cómo abro una cuenta de ahorros?")
print(response)

response = assistant.process_query("¿Cuál es la capital de Francia?")
print(response)