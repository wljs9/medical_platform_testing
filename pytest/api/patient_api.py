"""
接口层:患者模块
"""

import requests
from config import BASE_URL, TIMEOUT

HEADERS = {"Content-Type": "application/json"}

# 注意:数据库 patient.gender 是 enum('M','F'),
# 而接口直接透传不做校验 —— 这里用 'M' 保证创建成功
# (这是 DEF-001 缺陷的规避写法,用例层会专门测"传'男'应报错")


def list_patients():
    """GET /api/patients 全部患者(5万条,勿在自动化里反复调)"""
    return requests.get(f"{BASE_URL}/api/patients", timeout=TIMEOUT)


def create_patient(name, gender="M", birthDate="1990-01-01", phone="13900000001", idCard="110101199001011234"):
    """POST /api/patients 创建患者
    ⚠️ 参数名必须和后端 JSON 字段名一致(Java 实体的驼峰命名):
       birthDate / idCard —— 否则调用方传错 key 会 TypeError,传错会被后端静默丢弃。
    """
    body = {
        "name": name,
        "gender": gender,
        "birthDate": birthDate,
        "phone": phone,
        "idCard": idCard,
    }
    return requests.post(
        f"{BASE_URL}/api/patients", json=body, headers=HEADERS, timeout=TIMEOUT
    )


def get_patient(patient_id):
    """GET /api/patients/{id}"""
    return requests.get(f"{BASE_URL}/api/patients/{patient_id}", timeout=TIMEOUT)


def search_patients(name):
    """GET /api/patients/search?name=..."""
    return requests.get(f"{BASE_URL}/api/patients/search", params={"name": name}, timeout=TIMEOUT)


def update_patient(patient_id, body):
    """PUT /api/patients/{id}"""
    return requests.put(
        f"{BASE_URL}/api/patients/{patient_id}", json=body, headers=HEADERS, timeout=TIMEOUT
    )


def delete_patient(patient_id):
    """DELETE /api/patients/{id}"""
    return requests.delete(f"{BASE_URL}/api/patients/{patient_id}", timeout=TIMEOUT)


def count_patients():
    """GET /api/patients/count"""
    return requests.get(f"{BASE_URL}/api/patients/count", timeout=TIMEOUT)


def department_stats():
    """GET /api/patients/stats/department 科室患者统计"""
    return requests.get(f"{BASE_URL}/api/patients/stats/department", timeout=TIMEOUT)