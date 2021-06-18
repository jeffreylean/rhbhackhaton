from fastapi import FastAPI
from server.routes.form import router as FormRouter
from server.routes.model_configuration import router as ConfigurationRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(FormRouter, tags=["Form"], prefix="/form")
app.include_router(
    ConfigurationRouter, tags=["ModelConfiguration"], prefix="/configuration"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
