from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from app.session.session_layer import validate_session
from app.session.session_layer import create_random_session_string
from app import models
from app.database import engine, Session
from sqlalchemy.orm import session
import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.add_middleware(SessionMiddleware, secret_key="s4cr4t")


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/test_session")
async def test_session(
    request: Request, is_valid_session: bool = Depends(validate_session)
):
    if not is_valid_session:
        return RedirectResponse("/logout", status_code=303)
    return "Welcome to the protected route"


@app.post("/logout")
async def logout(request: Request, response: RedirectResponse):
    request.session.clear()
    response.delete_cookie(key="Authorization")
    return RedirectResponse("/login", status_code=303)


@app.post("/login")
async def login(request: Request, response: RedirectResponse):
    session_id = request.session["session_id"] = create_random_session_string()
    request.session["token_exp"] = datetime(2025, 05, 15)
    #store sesson id in redis or some db
    response.set_cookie('Authorization', 'session_id')

