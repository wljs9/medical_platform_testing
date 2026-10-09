"""
用例层夹具(conftest.py):pytest 的固定装置
作用:管理测试数据的前置准备与后置清理,保证用例可重复执行。
面试点:测试数据要"自给自足"——每条用例执行前造自己的数据,
      执行后清理,不依赖别人的残留,也不污染共享数据。
"""

import uuid
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import department_api, patient_api


@pytest.fixture(scope="function")
def new_department():
    """创建并命名唯一科室,用例用完后自动删除(后置清理)"""
    name = f"自动化科室_{uuid.uuid4().hex[:8]}"
    resp = department_api.create_department(name)
    assert resp.status_code == 200, f"前置创建科室失败: {resp.text}"

    # 查出刚创建的 id
    all_depts = department_api.list_departments().json()
    dept_id = None
    for d in all_depts:
        if d["departmentName"] == name:
            dept_id = d["departmentId"]
            break
    assert dept_id is not None, "未找到刚创建的科室"

    yield {"id": dept_id, "name": name}

    # 后置清理:删除测试科室(容忍删除失败——可能已被其他用例删了)
    try:
        department_api.delete_department(dept_id)
    except Exception:
        pass


@pytest.fixture(scope="function")
def new_patient():
    """创建唯一患者,用后自动清理"""
    uniq = uuid.uuid4().hex[:8]
    body = {
        "name": f"自动化患者_{uniq}",
        "gender": "M",
        "birthDate": "1990-01-01",
        "phone": f"139{uniq[:8]}",
        "idCard": f"{uniq[:4]}",
    }
    resp = patient_api.create_patient(**body)
    assert resp.status_code == 200, f"前置创建患者失败: {resp.text}"

    patients = patient_api.search_patients(f"自动化患者_{uniq}").json()
    pid = patients[0]["patientId"] if patients else None
    assert pid is not None, "未找到刚创建的患者"

    yield {"id": pid, "body": body}

    try:
        patient_api.delete_patient(pid)
    except Exception:
        pass