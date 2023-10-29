import db
import bcrypt
import jwt
from datetime import datetime,timedelta
from fastapi import HTTPException

SECRET_KEY = ""
ALGORITHM = ""

def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise str(e)
    
def check_if_user_exist(user_name):
    count_user="SELECT COUNT(*) FROM  user_table WHERE user_name ilike '"+str(user_name)+"';"
    count_user_data=db.perform_select_operation(count_user)
    count=count_user_data[0]['count'] 
    if(count>0): 
        return True
    return False

def register(name, email, password):
    try:
        if(check_if_user_exist(name)):
            return "user already registered"
        
        password_binary=password.encode('utf-8')
        salt=bcrypt.gensalt()
        hashed_password=str(bcrypt.hashpw(password_binary,salt))
        hashed_password_string=hashed_password[2:-1]
        
        insert_user="INSERT INTO user_table(user_name, user_email, password_hashed) VALUES('"+str(name)+"','"+str(email)+"','"+str(hashed_password_string)+"');"
        result=db.perform_iud_operation(insert_user)
        
        return result
    except Exception as e:
        return str(e)
    
def login(user_name, password):
    try:
        get_user_password = "SELECT password_hashed,user_name FROM user_table WHERE user_name ilike '" + str(user_name) + "';"
        hashed_password_data = db.perform_select_operation(get_user_password)
        hashed_password = hashed_password_data[0]["password_hashed"]
        user_name = hashed_password_data[0]["user_name"]
        if(not check_if_user_exist(user_name)):
            return "user not registered"

        hashed_password_binary = hashed_password.encode('utf-8')
        password_binary = password.encode('utf-8')

        if bcrypt.checkpw(password_binary, hashed_password_binary):
            user_data = {'user_name': user_name}
            access_token_expires = timedelta(hours=1)
            access_token = create_jwt_token(user_data, access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return "wrong password"
    except Exception as e:
        return str(e)
