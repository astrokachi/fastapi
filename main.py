from fastapi import FastAPI, HTTPException, Depends
import models
from database import engine, Session
from sqlalchemy.orm import session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("test-async")
async def read_results():
    results = await some_api()
    return results
