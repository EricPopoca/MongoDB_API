# MongoDB_API
Eric Muñoz Ledo Popoca
API creada para sincronizar con base de datos de MongoDB, taller de Tecnologías Disruptivas

## Crear un entorno virtual
En terminal:
- python -m venv venv

## Iniciar entorno virtual
Visual Code la mayoría de veces muestra un mensaje que permite que se cambie automaticamente; si ese no fuese el caso, en terminal:
- venv/Scripts/activate.bat             Para mensaje del sistema
- venv/Scripts/Activate.ps1             Para Powershell

## Instalar fastapi, uvicorn y pymongo
En terminal:
- python -m pip install fastapi
- python -m pip install uvicorn
- python -m pip install pymongo

## Para correr el programa
En terminal:

uvicorn Clientela:app --reload
Esto mostrará un link que llevara al sitio, este no tiene nada en el endpoint inicial, pero si se le agrega "/docs" se puede ver la documentación con los procesos completos, así como utilizarlos.

## Ver la conexión con Mongo
Se envió una invitación a su correo "chuisangel8@gmail.com" para ver el proyecto junto con sus cambios proyectables al usar el método post del API.