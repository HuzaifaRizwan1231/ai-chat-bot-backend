from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat_routes

# Initialize FastAPI app
app = FastAPI()

origins= [
    "http://localhost:5173",
]

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Routes
app.include_router(chat_routes.router, prefix="/api/chat")



  


    

