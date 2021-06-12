from fastapi import FastAPI
from server.routes.form import router as FormRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(FormRouter, tags=["Form"], prefix="/form")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
