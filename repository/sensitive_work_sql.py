from sqlalchemy.orm import Session
import data_models
import entity


def create_sensitive_work(db: Session, obj: str):
    db_obj = data_models.DemandSensitiveWord(badword=obj)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return


# 新增敏感字词
def delete_sensitive_work(db: Session, id: int):
    db_obj = db.query(data_models.DemandSensitiveWord).filter(data_models.DemandSensitiveWord.id == id).first()
    db.delete(db_obj)
    db.commit()
    return


def update_sensitive_work(db: Session, demandSensitiveWord: entity.DemandSensitiveWord):
    db_obj = db.query(data_models.DemandSensitiveWord).filter(
        data_models.DemandSensitiveWord.id == demandSensitiveWord.id).first()
    db_obj.badword = demandSensitiveWord.badword
    db.commit()



# 详情
def get_id_sensitive_work_detail(db: Session, id: int):
    return db.query(data_models.DemandSensitiveWord).filter(
        data_models.DemandSensitiveWord.id == id).first()


def get_by_id_sensitive_work_badword(db: Session, id: int):
    return db.query(data_models.DemandSensitiveWord).filter(
        data_models.DemandSensitiveWord.id == id).first()


def get_sensitive_work_all(db: Session):
    return db.query(data_models.DemandSensitiveWord.badword).all()


# 是否含有字词
def get_by_badword(db: Session, badword: str):
    return db.query(data_models.DemandSensitiveWord).filter(
        data_models.DemandSensitiveWord.badword == badword).first()


# 列表
def get_sensitive_work_list(db: Session, badword: str, size: int, page: int):
    if badword is not None:
        return db.query(data_models.DemandSensitiveWord).filter(
            data_models.DemandSensitiveWord.badword.like("%" + badword + "%")).offset(
            (page - 1) * size).limit(size).all()
    else:
        return db.query(data_models.DemandSensitiveWord).offset(
            (page - 1) * size).limit(size).all()
