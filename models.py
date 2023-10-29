from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Todo_Item(BaseModel):
    item_title: str
    item_description: str


class Delete_Todo_Item(BaseModel):
    item_id: int


class Update_Todo_Item(BaseModel):
    item_id: int
    item_title: str
    item_description: str
