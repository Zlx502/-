import yaml
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    with open('application.yaml', encoding='utf-8') as fs:
        data = yaml.load(fs, Loader=yaml.FullLoader)
        logins = data.get("LOGIN")
        user = logins.get(token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效身份凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: str = Depends(get_current_user)):
    disableaStatus = current_user.get("LOGIN_DISABLED_STATUS")
    userName = current_user.get("LOGIN_USERNAME")
    if not disableaStatus:
        raise HTTPException(status_code=400, detail=userName + "该账号已禁用！！")
    return current_user
