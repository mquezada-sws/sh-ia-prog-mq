## Explora
1. Crea un nuevo Chat con Cody.
2. 
- `@CAP02_CHALLENGE/app/main.py` Que hace esta app?
# Task Manager API - Explicación

## ¿Qué hace esta aplicación?

Esta aplicación es una **API de gestión de tareas** construida con FastAPI. Permite administrar tareas a través de una interfaz REST HTTP.

## Funcionalidad Principal

- **API REST para gestionar tareas**: Permite crear, leer, actualizar y eliminar tareas a través de endpoints HTTP
- **Arquitectura modular**: Usa routers separados para organizar mejor el código

## Componentes

### Endpoint Principal (`/`)
- Devuelve un mensaje de bienvenida: `{"message": "Task Manager API"}`
- Sirve como punto de entrada para verificar que la API esté funcionando

### Router de Tareas (`/tasks`)
- Todas las rutas relacionadas con tareas están bajo el prefijo `/tasks`
- Las operaciones específicas (crear, listar, actualizar, eliminar tareas) estarían definidas en el archivo `routers/tasks_router.py`
- Etiquetadas como "tasks" para la documentación automática

## Características de FastAPI

- **Documentación automática**: Genera docs interactivas en `/docs` y `/redoc`
- **Validación automática**: Valida tipos de datos automáticamente
- **Asíncrono**: Soporte nativo para operaciones asíncronas
- **Alto rendimiento**: Una de las frameworks más rápidas para Python

## Endpoints Típicos (probables)

Para ver todas las operaciones disponibles, tendrías que revisar el contenido del archivo `tasks_router.py`, pero típicamente incluiría endpoints como:

- `GET /tasks` - Listar tareas
- `POST /tasks` - Crear nueva tarea  
- `GET /tasks/{id}` - Obtener tarea específica
- `PUT /tasks/{id}` - Actualizar tarea
- `DELETE /tasks/{id}` - Eliminar tarea

## Estructura del Código

```python
from fastapi import FastAPI
from routers.tasks_router import tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Task Manager API"}
```

## Uso

1. Ejecutar la aplicación con `uvicorn main:app --reload`
2. Acceder a la documentación en `http://localhost:8000/docs`
3. Usar los endpoints para gestionar tareas


```
3.1 y 3.2 `@CAP02_CHALLENGE/app/routers/tasks_router.py` para que son los endpoints?
```

# Documentación de Endpoints - API de Tareas

Los endpoints en este código FastAPI son las rutas o puntos de acceso de tu API que permiten realizar operaciones CRUD (Create, Read, Update, Delete) sobre las tareas. Cada endpoint tiene un propósito específico:

## POST / - Crear tarea

```python
@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)
```

**Propósito:** Permite crear una nueva tarea enviando los datos en el cuerpo de la petición.

**Método HTTP:** `POST`

**Ruta:** `/`

**Parámetros:** 
- `task`: Objeto Task en el cuerpo de la petición

**Respuesta:** Devuelve la tarea creada con su ID asignado

---

## GET /{task_id} - Obtener tarea específica

```python
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**Propósito:** Recupera una tarea específica usando su ID.

**Método HTTP:** `GET`

**Ruta:** `/{task_id}`

**Parámetros:**
- `task_id`: ID de la tarea (entero)

**Respuesta:** 
- Éxito: Devuelve la tarea solicitada
- Error: HTTP 404 si la tarea no existe

---

## GET / - Obtener todas las tareas

```python
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)
```

**Propósito:** Devuelve una lista con todas las tareas almacenadas.

**Método HTTP:** `GET`

**Ruta:** `/`

**Parámetros:** Ninguno

**Respuesta:** Lista de todas las tareas en formato TaskList

---

## PUT /{task_id} - Actualizar tarea

```python
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task
```

**Propósito:** Modifica una tarea existente usando su ID y los nuevos datos proporcionados.

**Método HTTP:** `PUT`

**Ruta:** `/{task_id}`

**Parámetros:**
- `task_id`: ID de la tarea a actualizar (entero)
- `task_update`: Objeto UpdateTaskModel con los campos a modificar

**Respuesta:**
- Éxito: Devuelve la tarea actualizada
- Error: HTTP 404 si la tarea no existe

---

## DELETE /{task_id} - Eliminar tarea

```python
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}
```

**Propósito:** Elimina una tarea específica usando su ID.

**Método HTTP:** `DELETE`

**Ruta:** `/{task_id}`

**Parámetros:**
- `task_id`: ID de la tarea a eliminar (entero)

**Respuesta:** Mensaje de confirmación de eliminación exitosa

---

## Resumen

Estos endpoints forman una API REST completa para gestionar tareas, permitiendo a los clientes (aplicaciones web, móviles, etc.) interactuar con tu sistema de tareas a través de peticiones HTTP estándar. Cada endpoint maneja un aspecto diferente del ciclo de vida de las tareas en tu aplicación:

- **Crear**: Agregar nuevas tareas al sistema
- **Leer**: Consultar tareas individuales o todas las tareas
- **Actualizar**: Modificar tareas existentes
- **Eliminar**: Remover tareas del sistema

La API utiliza códigos de estado HTTP apropiados y maneja errores comunes como tareas no encontradas (404).

```
3.3 Como esta construida la base de datos?

```

Basándome en el código que proporcionado, no puedo determinar exactamente cómo está construida la base de datos porque:
1. Solo veo la capa de rutas - El código muestra los endpoints pero no la implementación de la base de datos
2. db es importado - Se importa desde un módulo db que no está visible
3. Métodos abstractos - Solo veo las llamadas a db.add_task(), db.get_task(), etc., pero no su implementación


# Como inicializar la aplicacion:
# 1. Asegúrate de tener FastAPI y Uvicorn instalados.
# 2. Guarda este código en un archivo llamado `main.py`.
# 3. Ejecuta el siguiente comando en tu terminal:
#    ```bash
#    uvicorn main:app --reload
#    ```
# 4. Abre tu navegador y ve a `http://127.0.0.1:8000`  para ver el mensaje de bienvenida.
# 5. Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`

## Corrige

1. `Code Smell Command`

```
1. Hardcoded Values (Magic Strings)
pythonif authorization != "Bearer your_token":
El token está hardcodeado directamente en el código, lo cual es una práctica muy insegura.
2. Inconsistent Error Handling

Las funciones get_task y update_task validan si el resultado es None y lanzan excepción
La función delete_task no valida si la tarea existe antes de eliminarla
delete_all_tasks no confirma si realmente se eliminaron las tareas

3. Poor Security Implementation

Autenticación muy básica con token hardcodeado
No hay validación real de autorización
Operación destructiva sin confirmación adicional

4. Missing Validation

delete_task no verifica si la tarea existe
delete_all_tasks no confirma cuántas tareas se eliminaron

5. Inconsistent Response Patterns

Algunas funciones retornan el objeto, otras retornan mensajes
No hay un patrón consistente para las respuestas