from fastapi import FastAPI
import app.models

from app.routes import transaction, category

app = FastAPI()

app.include_router(transaction.router, prefix="/transactions")
app.include_router(category.router, prefix="/categories")


@app.get("/")
def root():
    return {"message": "Hello World"}