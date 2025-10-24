from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post("/login", status_code=200)
def login(user):
    # Login operation here
    return user
