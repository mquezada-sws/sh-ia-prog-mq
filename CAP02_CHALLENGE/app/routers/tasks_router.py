import os
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Task, UpdateTaskModel, TaskList
from db import db
from typing import Optional

tasks_router = APIRouter()
security = HTTPBearer()

# Configuración desde variables de entorno
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "your_secure_token_here")

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica el token de administrador"""
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(
            status_code=403, 
            detail="Insufficient permissions for this operation"
        )
    return credentials.credentials

@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    """Crea una nueva tarea"""
    try:
        return db.add_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating task")

@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Obtiene una tarea por ID"""
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    """Obtiene todas las tareas"""
    try:
        tasks = db.get_tasks()
        return TaskList(tasks=tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving tasks")

@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    """Actualiza una tarea existente"""
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    """Elimina una tarea específica"""
    # Verificar que la tarea existe antes de eliminarla
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        success = db.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete task")
        return {"message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting task")

@tasks_router.delete("/")
async def delete_all_tasks(
    confirmation: str = Header(..., description="Must be 'DELETE_ALL_TASKS' to confirm"),
    token: str = Depends(verify_admin_token)
):
    """
    Elimina TODAS las tareas de la base de datos.
    Requiere autorización de administrador y confirmación explícita.
    """
    # Verificar confirmación explícita
    if confirmation != "DELETE_ALL_TASKS":
        raise HTTPException(
            status_code=400, 
            detail="Confirmation header must be 'DELETE_ALL_TASKS'"
        )
    
    try:
        # Obtener conteo actual antes de eliminar
        current_tasks = db.get_tasks()
        task_count = len(current_tasks) if current_tasks else 0
        
        if task_count == 0:
            return {"message": "No tasks to delete", "deleted_count": 0}
        
        # Realizar eliminación
        deleted_count = db.delete_all_tasks()
        
        # Verificar que se eliminaron todas las tareas
        remaining_tasks = db.get_tasks()
        if remaining_tasks and len(remaining_tasks) > 0:
            raise HTTPException(
                status_code=500, 
                detail="Failed to delete all tasks"
            )
        
        return {
            "message": "All tasks deleted successfully",
            "deleted_count": deleted_count or task_count,
            "confirmation": "Operation completed"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error during bulk deletion: {str(e)}"
        )