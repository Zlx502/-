import yaml
from fastapi import FastAPI, Depends, HTTPException, Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import entity
import response_format
from repository import sensitive_work_sql, record_data_sources_sql
import data_models
from sqlalchemy.orm import Session
from filtration import DFAFilter
from urllib import parse
import time
import uuid
from utils.login_util import get_current_active_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from database import SessionLocal, engine

data_models.Base.metadata.create_all(bind=engine)


# 连接数据库
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# 过滤敏感关键词
@app.post("/filterSensitiveWord", name="过滤敏感关键词", description="过滤敏感关键词")
def check_filter(request: Request, content: str, dataPackageId: Optional[str] = None, db: Session = Depends(get_db),
                 current_user: str = Depends(get_current_active_user)):
    data = sensitive_work_sql.get_sensitive_work_all(db)
    li = [] 
    for i, name in enumerate(data):
        li.append("|".join(data[i]))
    gfw = DFAFilter()
    gfw.parse(li)
    urlOrg = parse.unquote(content)  # 解码url
    result = gfw.filter(urlOrg)
    # 访问者ip
    ip = request.client.host
    # 转大写lower() 小写upper()
    if content == result or urlOrg.lower() == result.lower():
        # 记录数据来源
        record_data_sources_insert(content, dataPackageId, 0, 0, ip, db)
        return response_format.responseFormat()
    if urlOrg.lower() != result.lower():
        record_data_sources_insert(content, dataPackageId, 0, 1, ip, db)
        list = [{"content": content, "urlOrg": urlOrg, "result": result, "status": False}]
        return response_format.responseFormat(-9, "不能含有敏感字词！！", list)


# 新增记录数据来源
def record_data_sources_insert(content: str, dataPackageId: str, status: int, illegalStastu: int, ipAddress: str,
                               db: Session = Depends(get_db)):
    createAt: int = time.time()
    id = ''.join([each for each in str(uuid.uuid1()).split('-')])
    if dataPackageId is None:
        dataPackageId = ""
    recordDataSources = entity.RecordDataSourcesInsert(id=id,
                                                       ip_address=ipAddress,
                                                       content=content,
                                                       status=status,
                                                       data_package_id=dataPackageId,
                                                       illegal_stastu=illegalStastu,
                                                       create_at=createAt,
                                                       is_detele=0)
    record_data_sources_sql.create_record_data_sources(db, recordDataSources)


# 新增敏感字
@app.post("/sensitiveWordInsert", name="新增敏感词", description="新增敏感词")
def sensitive_word_insert(badword: str, db: Session = Depends(get_db),
                          current_user: str = Depends(get_current_active_user)):
    data = sensitive_work_sql.get_by_badword(db, badword)
    if data is not None:
        return response_format.responseFormat(-9, badword + "字段已存在")
    sensitive_work_sql.create_sensitive_work(db, badword)
    return response_format.responseFormat()


# 敏感字详情
@app.get("/sensitiveWordDateil", name="敏感字详情", description="敏感字详情")
def sensitive_word_dateil(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_active_user)):
    data = sensitive_work_sql.get_id_sensitive_work_detail(db, id)
    dataTwo = response_format.response_sensitive_work(data)
    return response_format.responseFormat(0, "succeed", dataTwo)


# 敏感字列表
@app.get("/sensitiveWordList", name="敏感字列表", description="敏感字列表")
def sensitive_word_list(size: int = 10, page: int = 1, badword: Optional[str] = None, db: Session = Depends(get_db),
                        current_user: str = Depends(get_current_active_user)):
    if page == 0:
        page = 1
    data = sensitive_work_sql.get_sensitive_work_list(db, badword, size, page)
    dataList = response_format.response_sensitive_work_list(data)
    return response_format.responseFormat(0, "succeed", dataList)


# 敏感字编辑
@app.post("/ensitiveWordUpdate", name="敏感字编辑", description="敏感字编辑")
def sensitive_word_upd(demandSensitiveWord: entity.DemandSensitiveWord, db: Session = Depends(get_db),
                       current_user: str = Depends(get_current_active_user)):
    data = sensitive_work_sql.get_by_badword(db, demandSensitiveWord.badword)
    if data is not None and (data.id == demandSensitiveWord.id):
        return response_format.responseFormat(-9, demandSensitiveWord.badword + "字段已存在")
    else:
        return response_format.responseFormat(-9, "不存在")
    sensitive_work_sql.update_sensitive_work(db, demandSensitiveWord)
    return response_format.responseFormat(0, "succeed")


# 删除敏感字
@app.post("/sensitiveWordDel", name="删除敏感字", description="删除敏感字")
def sensitive_word_del(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_active_user)):
    data = sensitive_work_sql.get_id_sensitive_work_detail(db, id)
    if data is not None:
        sensitive_work_sql.delete_sensitive_work(db, id)
        return response_format.responseFormat(0, "succeed")
    else:
        return response_format.responseFormat(0, "succeed")


# 登入才能使用其他api
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
