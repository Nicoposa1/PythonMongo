from fastapi import FastAPI
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Obtener las variables de entorno
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
raw_uri = os.getenv("ATLAS_URI")

if not username or not password or not raw_uri:
    raise ValueError("No ATLAS_URI, MONGO_USERNAME or MONGO_PASSWORD found in environment variables")

# Escapar el usuario y la contraseña
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# Reemplazar en la URI
escaped_uri = raw_uri.replace("<username>", escaped_username).replace("<password>", escaped_password)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(escaped_uri)
    app.database = app.mongodb_client[os.getenv("DB_NAME")]  # Asigna la base de datos a app.database
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"Message": "Hello world!"}

# Incluye tu router con un prefijo para la API
from routes import router as book_router
app.include_router(book_router, tags=["books"], prefix="/book")


