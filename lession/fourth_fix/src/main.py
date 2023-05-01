from fastapi import FastAPI, Depends
from auth.base_config import User, current_user

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from operations.router import router as router_operation

app = FastAPI(
    title="TriPic"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Привет, {user.username} !"

@app.get("/unprotected-route")
def protected_route():
    return f"Аноним! Вы не зарегистрированы"