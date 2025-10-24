from fastapi import FastAPI
from auth.router import auth_router

app = FastAPI()
app.include_router(auth_router, prefix="auth")

@app.get("/health")
def root():
    return {"message": "Server is Healthy"}