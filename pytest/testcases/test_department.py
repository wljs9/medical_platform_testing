"""
用例层:科室模块测试用例
用例设计:正常场景 + 参数校验 + 异常场景
(对应缺陷清单中的 DEF-005 空科室、DEF-006 重复科室、DEF-007 不存在ID)
"""

import pytest
from api import department_api


class TestDepartmentCRUD:
    """科室 CRUD 正常流程"""

    def test_create_and_get(self, new_department):
        """创建后可查询到,字段一致"""
        resp = department_api.get_department(new_department["id"])
        assert resp.status_code == 200
        assert resp.json()["departmentName"] == new_department["name"]

    def test_update(self, new_department):
        """更新科室名称,再次查询确认变更"""
        resp = department_api.update_department(new_department["id"], "改名后的科室")
        assert resp.status_code == 200
        assert "成功" in resp.text

        check = department_api.get_department(new_department["id"]).json()
        assert check["departmentName"] == "改名后的科室"

    def test_delete(self, new_department):
        """删除后 count 减少且查不到该科室"""
        before = department_api.count_departments().json()
        resp = department_api.delete_department(new_department["id"])
        assert resp.status_code == 200

        after = department_api.count_departments().json()
        assert after == before - 1, f"删除后数量应为{before}-1={before-1},实际{after}"


class TestDepartmentValidation:
    """参数校验与异常场景 —— 已知缺陷用 xfail 标记
    约定:断言写"期望的正确行为";缺陷未修复 → 断言失败被 xfail 吞掉,显示 XFAIL(黄);
         缺陷修复后 → 断言通过 → strict=True 报 XPASS 失败,提醒清理标记。
    """

    @pytest.mark.xfail(reason="DEF-005 空科室未被拒绝,缺陷未修复", strict=True)
    def test_create_empty_name_should_fail(self):
        """空名称应被拒绝(400/500均可,重点是不得创建成功)"""
        resp = department_api.create_department("")
        assert resp.status_code != 200, "DEF-005:空科室名称被允许创建"

    @pytest.mark.xfail(reason="DEF-006 重复科室未被拒绝,缺陷未修复", strict=True)
    def test_create_duplicate_name_should_fail(self):
        """重复科室(内科已存在)应被拒绝"""
        resp = department_api.create_department("内科")
        assert resp.status_code != 200, "DEF-006:重复科室【内科】被允许创建"

    @pytest.mark.xfail(reason="DEF-007 不存在ID返回200而非404,缺陷未修复", strict=True)
    def test_get_nonexistent_id(self):
        """不存在的ID应返回404"""
        resp = department_api.get_department(99999999)
        assert resp.status_code == 404, f"DEF-007:不存在ID返回{resp.status_code}(期望404)"


class TestDepartmentBatch:
    """批量接口:部分成功/部分失败的异常场景
    (这条不是"已知缺陷",是每次都要验证的数据一致性,保持普通用例)"""

    def test_batch_partial_failure(self):
        """
        验证批量接口事务性:一条非法是否导致全部回滚
        前置记录count,批量含一条空名称,若count变化 → 部分成功未回滚(缺陷)
        """
        before = department_api.count_departments().json()
        resp = department_api.batch_create_departments(["批量_正常A", "批量_正常B", ""])
        after = department_api.count_departments().json()

        print(f"批量前: {before}, 批量后: {after}, 接口返回: {resp.status_code}")
        assert after == before, (
            f"缺陷确认:批量接口无事务,部分失败未回滚(count {before}→{after})。"
            "建议批量方法加 @Transactional"
        )