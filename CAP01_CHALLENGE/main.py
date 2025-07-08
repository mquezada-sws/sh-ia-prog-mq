from fastapi import Depends, FastAPI, HTTPException
from typing import List
from fastapi.params import Query
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt

fake_db = {"users": {}}
SECRET_KEY = "4di2X1BVj0EgwnYzkVdNgqL1LF2bwGlg"
ALGORITHM = "HS256"

app = FastAPI()


class Payload(BaseModel):
    numbers: List[int]


class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

# quiero proteger los endpoints recibiendo un un parámetro token que sea un JWT, si el token no es válido se debe retornar un error 401
def get_current_user(token: str = Query(None, alias="token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_db["users"]:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

#quiero un endpoint que reciba un payload con una lista de numeros y retorne la suma de los numeros
@app.post("/sum")
def sum_numbers(payload: Payload, token: str = Depends(get_current_user)):
    """
    Calculates the sum of a list of numbers provided in the payload.

    Args:
        payload (Payload): An object containing a list of numbers to sum.
        token (str, optional): The authentication token of the current user, injected by dependency.

    Raises:
        HTTPException: If the list of numbers is empty, raises a 400 Bad Request error.

    Returns:
        dict: A dictionary containing the sum of the numbers, with the key 'sum'.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    return {"sum": sum(payload.numbers)}

#quiero un endpoint  Recibe una lista de números y devuelve la lista ordenada utilizando el algoritmo de Bubble Sort su ruta es /bubble-sort
@app.post("/bubble-sort")
def bubble_sort(payload: Payload, token: str = Depends(get_current_user)):
    """
    Sorts a list of numbers in ascending order using the bubble sort algorithm.

    Args:
        payload (Payload): An object containing a list of numbers to be sorted.
        token (str, optional): The authentication token for the current user, injected via dependency.

    Raises:
        HTTPException: If the list of numbers is empty.

    Returns:
        dict: A dictionary containing the sorted list of numbers under the key 'sorted_numbers'.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return {"sorted_numbers": numbers}

# Filtro de Pares
@app.post("/filter-even")
def filter_even_numbers(payload: Payload, token: str = Depends(get_current_user)):
    """
    Filters even numbers from the provided payload.

    Args:
        payload (Payload): An object containing a list of numbers to filter.
        token (str, optional): Authentication token obtained via dependency injection. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the list of numbers in the payload is empty.

    Returns:
        dict: A dictionary with a single key "even_numbers" containing a list of even numbers from the payload.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    even_numbers = [num for num in payload.numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}

# Quiero un endpoint que Recibe una lista de números y devuelve la suma de sus elementos., su entrada es {"numbers": [lista de números]} y su salida  {"sum": suma de los números}
@app.post("/sum")
def sum_numbers(payload: Payload, token: str = Depends(get_current_user)):
    """
    Calculates the sum of a list of numbers provided in the payload.

    Args:
        payload (Payload): An object containing a list of numbers to sum.
        token (str, optional): The authentication token of the current user, injected by dependency.

    Returns:
        dict: A dictionary with the key "sum" and the value as the sum of the numbers.

    Raises:
        HTTPException: If the list of numbers in the payload is empty, raises a 400 error.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    return {"sum": sum(payload.numbers)}

#Quiero un endpoint que reciba un payload con una lista de números y  devuelva el mumero mas grande de la lista
@app.post("/max-value")
def max_value(payload: Payload, token: str = Depends(get_current_user)):
    """
    Finds the maximum value in a list of numbers provided in the payload.

    Args:
        payload (Payload): An object containing a list of numbers to evaluate.
        token (str, optional): The authentication token for the current user, injected via dependency.

    Raises:
        HTTPException: If the list of numbers in the payload is empty.

    Returns:
        dict: A dictionary containing the maximum value found in the list, with the key 'max'.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    return {"max": max(payload.numbers)}

# quiero un endpoint que Recibe un número y una lista de números ordenados. Devuelve true y el índice si el número está en la lista, de lo contrario false y -1 como índice.
@app.post("/binary-search")
def binary_search(payload: BinarySearchPayload, token: str = Depends(get_current_user)):
    """
    Performs a binary search on a sorted list of numbers to find the target value.

    Args:
        payload (BinarySearchPayload): An object containing a sorted list of numbers (`numbers`) and the target value (`target`) to search for.
        token (str, optional): The authentication token for the current user, injected by dependency (`Depends(get_current_user)`).

    Raises:
        HTTPException: If the list of numbers is empty, raises a 400 Bad Request error.

    Returns:
        dict: A dictionary with keys:
            - "found" (bool): True if the target is found, False otherwise.
            - "index" (int): The index of the target in the list if found, otherwise -1.
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    low = 0
    high = len(payload.numbers) - 1
    while low <= high:
        mid = (low + high) // 2
        if payload.numbers[mid] == payload.target:
            return {"found": True, "index": mid}
        elif payload.numbers[mid] < payload.target:
            low = mid + 1
        else:
            high = mid - 1
    return {"found": False, "index": -1}


# Quierro agregar un endpoint que permita registrar un usuario con su contraseña, la contraseña debe ser hasheada antes de guardarla

@app.post("/register")
def register(username: str, password: str):
    """
    Registers a new user with the provided username and password.
    Args:
        username (str): The desired username for the new user.
        password (str): The password for the new user.
    Raises:
        HTTPException: If the username already exists in the database.
    Returns:
        dict: A message indicating successful user registration.
    """
    if username in fake_db["users"]:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = CryptContext(schemes=["bcrypt"]).hash(password)
    fake_db["users"][username] = hashed_password
    return {"message": "User registered successfully"}
    
# Quiero agregar autenticación a los endpoints, para esto quiero un endpoint que reciba un usuario y una contraseña y retorne un token de autenticación
@app.post("/login")
def login(username: str, password: str):
    """
Handles user login by verifying credentials and generating a JWT access token.
Args:
    username (str): The username provided by the user.
    password (str): The password provided by the user.
Raises:
    HTTPException: If the username does not exist or the password is incorrect, raises a 401 Unauthorized error.
Returns:
    dict: A dictionary containing the JWT access token and its type.
"""
    if username not in fake_db["users"] or not CryptContext(schemes=["bcrypt"]).verify(password, fake_db["users"][username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

