from auth import authRouter
from auth.auth_middleware import AuthMiddleware
from crud import crudRouter
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(authRouter)
app.include_router(crudRouter)

@app.on_event("startup")
def on_startup():
    from dependencies.database import init_db
    init_db()