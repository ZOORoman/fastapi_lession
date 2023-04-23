from fastapi import FastAPI

app = FastAPI(
    title="TriPic"
)

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "triper", "name": "Robert"},
    {"id": 3, "role": "hiker", "name": "Sergey"},
]

@app.get("/")
def get_hello():
    return "Hello world"

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

fake_avia = [
    {"id": 1, "user_id": 1, "from": "Moscow", "to": "Milan", "price": 7854, "status": "X"},
    {"id": 2, "user_id": 1, "from": "Moscow", "to": "Berlin", "price": 13567, "status": " "},
    {"id": 3, "user_id": 1, "from": "Moscow", "to": "Barcelona", "price": 11503, "status": "X"},
]

@app.get("/avia")
def get_avia(limit: int = 10, offset: int = 0):
    return fake_avia[offset:][:limit]


fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "triper", "name": "Robert"},
    {"id": 3, "role": "hiker", "name": "Sergey"},
]

@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}