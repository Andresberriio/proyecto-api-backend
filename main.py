
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import producto_routes

app = FastAPI(
    title="API de Productos",
    description="Una API modular para gestionar productos (CRUD)",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
   
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(producto_routes.router)

@app.get("/")
def read_root():
    return {"bienvenido": "API de Productos funcionando correctamente"}