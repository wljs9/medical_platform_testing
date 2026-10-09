"""
接口层:科室模块 —— 每个业务接口一个函数。
作用:把 requests 的细节(拼接URL、请求头、超时)从用例层剥离。
面试点:用例层只关心"调用 + 断言",接口怎么发的封装在这里,
      接口实现变了(如从 GET 改 POST)只改这一层,用例不动。
"""

import requests
from config import BASE_URL, TIMEOUT

HEADERS = {"Content-Type": "application/json"}


def list_departments():
    """GET /api/departments 查询全部科室"""
    resp = requests.get(f"{BASE_URL}/api/departments", timeout=TIMEOUT)
    return resp


def get_department(dept_id):
    """GET /api/departments/{id} 按ID查询科室"""
    resp = requests.get(f"{BASE_URL}/api/departments/{dept_id}", timeout=TIMEOUT)
    return resp


def create_department(name):
    """POST /api/departments 创建科室"""
    resp = requests.post(
        f"{BASE_URL}/api/departments",
        json={"departmentName": name},
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    return resp


def batch_create_departments(names):
    """POST /api/departments/batch 批量创建科室"""
    body = [{"departmentName": n} for n in names]
    resp = requests.post(
        f"{BASE_URL}/api/departments/batch",
        json=body,
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    return resp


def update_department(dept_id, name):
    """PUT /api/departments/{id} 更新科室名称"""
    resp = requests.put(
        f"{BASE_URL}/api/departments/{dept_id}",
        json={"departmentName": name},
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    return resp


def delete_department(dept_id):
    """DELETE /api/departments/{id} 删除科室"""
    resp = requests.delete(f"{BASE_URL}/api/departments/{dept_id}", timeout=TIMEOUT)
    return resp


def count_departments():
    """GET /api/departments/count 科室总数"""
    resp = requests.get(f"{BASE_URL}/api/departments/count", timeout=TIMEOUT)
    return resp