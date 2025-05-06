from fastapi import FastAPI, HTTPException, Depends
from models import Message


app = FastAPI()

@app.get('/')
def root():
    return { 'message': 'hello world' }