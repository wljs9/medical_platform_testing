
import pytest
from api import patient_api

class TestPatientCRUD:
    @pytest.mark.api
    def test_insert(self,new_patient):
        res=patient_api.get_patient(new_patient["id"])
        assert res.status_code==200
        assert res.json()["phone"]==new_patient["body"]["phone"]

    @pytest.mark.api
    def test_search(self,new_patient):
        res=patient_api.search_patients(new_patient["body"]["name"])
        assert res.status_code==200
        assert res.json()[0]["name"]==new_patient["body"]["name"]

    @pytest.mark.api
    def test_update(self,new_patient):
        body={
        "name": "测试1",
        "gender": "M",
        "birthDate": "1990-01-01",
        "phone": "13900000001",
        "idCard": "1000050002"
        }
        res=patient_api.update_patient(new_patient["id"],body)
        assert res.status_code==200
        check=patient_api.get_patient(new_patient["id"])
        assert check.json()["name"]=="测试1"

    @pytest.mark.api
    @pytest.mark.xfail(reason="DEF-004:删除有关联病历/检查的患者应成功,实际被外键拦截(500/1451)", strict=True)
    def test_delete_patient_with_records(self, new_patient):
        """先挂一条病历 + 一条检查,再造出有子记录的状态,再删应该成功"""
        # 前置:给患者创建病历和检查(挂关联)
        mr = patient_api.create_medical_record(
            new_patient["id"], doctor_id=1,
            symptoms="测试症状", diagnosis="测试诊断")
        assert mr.status_code == 200, "前置:创建病历失败"
        er = patient_api.create_examination_request(
            new_patient["id"], doctor_id=1,
            examination_type="血常规", status="pending")
        assert er.status_code == 200, "前置:创建检查失败"

        # 真正要验证的行为:删有子记录的患者应该成功
        res = patient_api.delete_patient(new_patient["id"])
        assert res.status_code == 200