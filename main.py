from fastapi import FastAPI
from pymongo import MongoClient
from urllib.parse import quote_plus

app = FastAPI()

uri = "mongodb+srv://<username>:<password>@cluster0.zaxvna2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
escaped_uri = uri.replace("<username>", quote_plus("nicoposa57@gmail.com")).replace("<password>", quote_plus("BZ8XzVoMnNVeUz84"))

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(escaped_uri)
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"Message" : "Hello world!"}
