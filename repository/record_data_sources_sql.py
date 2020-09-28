from sqlalchemy.orm import Session

import entity
import data_models


def create_record_data_sources(db: Session, recordDataSources: entity.RecordDataSourcesInsert):
    db_obj = data_models.RecordDataSources(id=recordDataSources.id,
                                           ip_address=recordDataSources.ip_address,
                                           content=recordDataSources.content,
                                           status=recordDataSources.status,
                                           data_package_id=recordDataSources.data_package_id,
                                           illegal_stastu=recordDataSources.illegal_stastu,
                                           create_at=recordDataSources.create_at,
                                           is_detele=recordDataSources.is_detele)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return
