from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    raise RuntimeError("Missing Supabase environment variables")

supabase: Client = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    email: str


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    message: str
    user: Any | None = None


@app.post("/register", response_model=RegisterResponse)
def register_user(data: RegisterRequest):
    try:
        response = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    user = None
    if isinstance(response, dict):
        user = response.get("user")
    else:
        user = getattr(response, "user", None)

    if user is None:
        raise HTTPException(status_code=400, detail="Registration failed")

    return {"message": "User registered successfully"}