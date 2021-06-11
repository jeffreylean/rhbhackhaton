from fastapi import FastAPI
from server.routes.form import router as FormRouter

app = FastAPI()

app.include_router(FormRouter, tags=["Form"], prefix="/form")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "welcome"}
