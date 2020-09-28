from typing import Optional


# {"code":"","msg":"","data":{"":""}}
# 响应格式
def responseFormat(code: int = 0, msg: str = "succeed", data: Optional[object] = None):
    formatReturn = {"code": code, "msg": msg, "data": data}
    return formatReturn


def response_sensitive_work_list(data: Optional[object] = None):
    listData = []
    for i in range(len(data)):
        listData.append(
            {
                'id': data[i].id,
                'badword': data[i].badword
            }
        )
    return listData


def response_sensitive_work(data: Optional[object] = None):
    listData = [{"data": data.id, "badword": data.badword}]
    return listData
