# API creada por Eric Muñoz Ledo Popoca #

# Importación de elementos necesarios
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Modelo de datos para cliente #
class Cliente(BaseModel):
    id: int        # Numero de identificación
    nombre: str        
    edad: int
    correo: str        

# Crear aplicación #
app = FastAPI()

# Conexión a MongoDB Remoto #
MONGO_URI = "mongodb+srv://Popoca:palito13@clientela.daz2x.mongodb.net/?retryWrites=true&w=majority&appName=Clientela"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["clientes_db"]                  # Nombre de la base de datos #
clientes_collection = db["clientes"]        # Nombre de la colección #

# Crear cliente #
@app.post("/clientes/", response_model=Cliente)
def crear_cliente(cliente: Cliente):
    if clientes_collection.find_one({"id": cliente.id}):        # Verificar que el id no se repita #
        raise HTTPException(status_code=400, detail="id ya existente.")
    clientes_collection.insert_one(cliente.dict())              # Insertar cliente en MongoDB #
    return cliente

# Get para clientes #
@app.get("/clientes/", response_model=List[Cliente])
def obtener_clientes():
    clientes = list(clientes_collection.find({}, {"_id": 0}))   # Excluir el campo _id #
    return clientes

# Buscar un cliente por id #
@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    cliente = clientes_collection.find_one({"id": cliente_id}, {"_id": 0})  # Excluir el campo _id #
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado.")

# Editar información de cliente #
@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente_actualizado: Cliente):
    resultado = clientes_collection.update_one({"id": cliente_id}, {"$set": cliente_actualizado.dict()})
    if resultado.matched_count:
        return cliente_actualizado
    raise HTTPException(status_code=404, detail="Cliente inexistente.")

# Eliminar cliente #
@app.delete("/clientes/{cliente_id}", response_model=Cliente)
def eliminar_cliente(cliente_id: int):
    cliente = clientes_collection.find_one_and_delete({"id": cliente_id}, {"projection": {"_id": 0}})  # Excluir el campo _id #
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente inexistente.")
