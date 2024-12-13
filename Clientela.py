# API creada por Eric Muñoz Ledo Popoca #

#Importación de elementos necesario
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

# Modelo de datos para cliente #
class Cliente(BaseModel):
    id: int        #Numero de identificación
    nombre: str        
    edad: int
    correo: str        

# Crear aplicación #
app = FastAPI()

# Para el guardado de datos se crea el archivo JSON, de otra forma los datos se borran cuando se cierre el programa #
DATA_FILE = "clientes.json"

# Base de datos local #
clientes_db : List[Cliente] = []

# Carga y guardado de datos del JSON a la memoria local #
# Cargar datos #
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            datos = json.load(file)
            return [Cliente(**cliente) for cliente in datos]
    return []

# Guardar datos #
def guardar_datos():
    with open(DATA_FILE, "w") as file:
        json.dump([cliente.dict() for cliente in clientes_db], file, indent=4)

# Inicializar la base de datos #
clientes_db = cargar_datos()

# Crear cliente #
@app.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente: Cliente):
    for existente in clientes_db:                        # Verificar que el id no se repita #
        if existente.id == cliente.id:
            raise HTTPException(status_code=400, detail="id ya existente.")
    clientes_db.append(cliente)
    guardar_datos()                                     # Guardar datos en JSON #
    return cliente

# Get para clientes #
@app.get("/clientes/", response_model=List[Cliente])
def obtener_clientes():
    return clientes_db

# Buscar un cliente por id #
@app.get("/clientes/{clientes_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cliente in clientes_db:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado.")

# Editar información de cliente #
@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente_actualizado: Cliente):
    for index, cliente in enumerate(clientes_db):
        if cliente.id == cliente_id:
            clientes_db[index] = cliente_actualizado
            guardar_datos()
            return cliente_actualizado
    raise HTTPException(status_code=404, detail="Cliente inexistente.")

# Eliminar cliente #
@app.delete("/clientes/{cliente_id}", response_model=Cliente)
def eliminar_cliente(cliente_id: int):
    for index, cliente in enumerate(clientes_db):
        if cliente.id == cliente_id:
            eliminado = clientes_db.pop(index)
            guardar_datos()
            return eliminado
    raise HTTPException(status_code=404, detail="Cliente inexistente.")