from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json


app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# start server : uvicorn main:app --reload
@app.get("/")
async def root():
    f = open('chatLog.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    return data