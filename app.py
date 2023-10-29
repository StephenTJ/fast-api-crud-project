from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends
from typing_extensions import Annotated
import models as md
import login as ln
import todo as td


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register",tags=['Authentication'])
def register(user: md.UserRegister):
    try:
        name = user.name
        email = user.name
        password = user.password
        result = ln.register(name, email, password)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login",tags=['Authentication'])
def login(user: md.UserLogin):
    try:
        user_name = user.username
        password = user.password
        result = ln.login(user_name, password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/token",tags=['Authentication'])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_name = form_data.username
        password = form_data.password
        result = ln.login(user_name, password)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/add_todo_item",tags=['CRUD Operation'])
def add_todo_item(todo_item: md.Todo_Item, token: str = Depends(oauth2_scheme)):
    try:
        payload = ln.decode_jwt_token(token)
        user_name = payload['user_name']
        item_title = todo_item.item_title
        item_discription = todo_item.item_description
        result = td.add_todo_item(user_name, item_title, item_discription)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_todo_items",tags=['CRUD Operation'])
def get_todo_items(token: str = Depends(oauth2_scheme)):
    try:
        payload = ln.decode_jwt_token(token)
        user_name = payload['user_name']
        result = td.get_todo_items(user_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/delete_todo_item",tags=['CRUD Operation'])
def delete_todo_item(delete_todo_item: md.Delete_Todo_Item, token: str = Depends(oauth2_scheme)):
    try:
        payload = ln.decode_jwt_token(token)
        user_name = payload['user_name']
        item_id = delete_todo_item.item_id
        result = td.delete_todo_item(user_name, item_id)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/update_todo_item",tags=['CRUD Operation'])
def update_todo_item(update_todo_item: md.Update_Todo_Item, token: str = Depends(oauth2_scheme)):
    try:
        payload = ln.decode_jwt_token(token)
        user_name = payload['user_name']
        item_id = update_todo_item.item_id
        item_title = update_todo_item.item_title
        item_discription = update_todo_item.item_description
        result = td.update_todo_item(
            user_name, item_id, item_title, item_discription)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/",tags=['Hello World'])
def hello():
    return {"Assignement": "Stephen Jose"}
