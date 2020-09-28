from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DemandSensitiveWord(Base):
    __tablename__ = "demand_sensitive_word"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    badword = Column(String)


class RecordDataSources(Base):
    __tablename__ = "record_data_sources"
    id = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    content = Column(String, nullable=True)
    status = Column(String, default=0)
    data_package_id = Column(String, nullable=True)
    illegal_stastu = Column(Integer, nullable=True, default=0)
    create_at = Column(Integer, nullable=True)
    update_at = Column(Integer, nullable=True)
    is_detele = Column(Integer, nullable=True, default=0)
    detele_at = Column(Integer, nullable=True)
