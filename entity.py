from typing import List, Optional

from pydantic import BaseModel


class DemandSensitiveWord(BaseModel):
    id: int
    badword: str


class RecordDataSourcesInsert(BaseModel):
    id: str
    ip_address: str
    content: str
    status: str
    data_package_id: str
    illegal_stastu: int
    create_at: int
    is_detele: int
    name: Optional[str] = None
    update_at: Optional[int] = None
    detele_at: Optional[int] = None
