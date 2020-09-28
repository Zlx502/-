
import yaml
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.login_util import get_current_active_user

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", name="登入使用文档", description="文档登入", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with open('application.yaml', encoding='utf-8') as fs:
        data = yaml.load(fs, Loader=yaml.FullLoader)
        logins = data.get("LOGIN")
        user_dict = logins.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="用户名或密码不正确")
    userName = user_dict.get("LOGIN_USERNAME")
    userPass = user_dict.get("LOGIN_PASSWORD")
    hashed_password: str = form_data.password
    if not hashed_password == str(userPass):
        raise HTTPException(status_code=400, detail="用户名或密码不正确")
    return {"access_token": userName, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_active_user)):
    return


@app.get("/users/me1")
async def read_users_me():
    with open('application.yaml', encoding='utf-8') as fs:
        data = yaml.load(fs, Loader=yaml.FullLoader)
        SQLALCHEMY_DATABASE_URL = data.get("LOGIN")
    return SQLALCHEMY_DATABASE_URL[1]
