from fastapi import FastAPI
from routers.tasks_router import tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


@app.get("/")
async def root():
    return {"message": "Task Manager API"}


# Como inicializar la aplicacion:
# 1. Asegúrate de tener FastAPI y Uvicorn instalados.
# 2. Guarda este código en un archivo llamado `main.py`.
# 3. Ejecuta el siguiente comando en tu terminal:
#    ```bash
#    uvicorn main:app --reload
#    ```
# 4. Abre tu navegador y ve a `http://127.0.0.1:8000`  para ver el mensaje de bienvenida.
# 5. Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`