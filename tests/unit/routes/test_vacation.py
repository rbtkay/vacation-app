import uuid
from tests.factories import VacationFactory
from datetime import date
from datetime import timedelta


class TestVacationGetEndpoint:
    def test_get_nominal(self, client, session):
        vacation = VacationFactory(session).create()

        response = client.get(f"/vacation/{vacation.id}")
        assert response.status_code == 200

    def test_get_404(self, client):
        response = client.get(f"/vacation/{uuid.uuid4()}")
        assert response.status_code == 404


class TestVacationPostEndpoints:
    def test_post_nominal(self, client, session):
        vacation = VacationFactory(session).create()

        payload = {
            "start_date": str(date(2000, 1, 1)),
            "end_date": str(date(2000, 1, 5)),
            "employee_id": str(vacation.employee.id),
            "vacation_type": "paid leave",
        }

        response = client.post(f"/vacation", json=payload)
        assert response.status_code == 201
    
    def test_post_raises_404_when_employee_none(self, client, session):
        VacationFactory(session).create(employee=None)

        payload = {
            "start_date": str(date(2000, 1, 1)),
            "end_date": str(date(2000, 1, 5)),
            "employee_id": str(uuid.uuid4()),
            "vacation_type": "paid leave",
        }

        response = client.post(f"/vacation", json=payload)
        assert response.status_code == 404
    
    def test_post_raises_400_if_dates_are_wrong(self, client, session):
        vacation = VacationFactory(session).create()

        payload = {
            "start_date": str(date(2000, 1, 5)),
            "end_date": str(date(2000, 1, 1)),
            "employee_id": str(vacation.employee_id),
            "vacation_type": "paid leave",
        }

        response = client.post(f"/vacation", json=payload)
        assert response.status_code == 422
    
    def test_post_raises_422_if_type_is_wrong(self, client, session):
        vacation = VacationFactory(session).create(employee=None)

        payload = {
            "start_date": str(date(2000, 1, 1)),
            "end_date": str(date(2000, 1, 5)),
            "employee_id": str(vacation.employee_id)
        }

        response = client.post(f"/vacation", json=payload)
        assert response.status_code == 422
    
    def test_post_raises_400_if_overlapping_of_other_type(self, client, session):
        start_date = date(1900, 1, 1)
        end_date = date(1900, 1, 10)
        vacation_existing = VacationFactory(session).create(
            start_date=start_date,
            end_date=end_date,
            vacation_type='paid leave',
        )

        payload = {
            "start_date": str(start_date - timedelta(days=2)),
            "end_date": str(end_date - timedelta(days=2)),
            "employee_id": str(vacation_existing.employee_id),
            "vacation_type": 'unpaid leave',
        }

        response = client.post(f"/vacation", json=payload)
        assert response.status_code == 400
    
class TestVacationPatchEndpoints:
    def test_patch_nominal(self, client, session):
        vacation = VacationFactory(session).create()

        new_start_date = str(date(2000, 1, 1))
        new_end_date = str(date(2000, 1, 5))
        
        payload = {
            "start_date": new_start_date,
            "end_date": new_end_date,
            "vacation_type": "paid leave",
        }

        response = client.patch(f"/vacation/{vacation.id}", json=payload)
        assert response.status_code == 200

        response_data = response.json()
        assert response_data['id'] == str(vacation.id)
        assert response_data['start_date'] == new_start_date
        assert response_data['end_date'] == new_end_date
    
    def test_patch_raises_404_when_vacation_not_found(self, client, session):
        new_start_date = str(date(2000, 1, 1))
        new_end_date = str(date(2000, 1, 5))
        
        payload = {
            "start_date": new_start_date,
            "end_date": new_end_date,
            "vacation_type": "paid leave",
        }

        response = client.patch(f"/vacation/{uuid.uuid4()}", json=payload)
        assert response.status_code == 404
    
    def test_patch_raises_422_if_dates_are_wrong(self, client, session):
        vacation = VacationFactory(session).create(employee=None)

        payload = {
            "start_date": str(date(2000, 1, 5)),
            "end_date": str(date(2000, 1, 1)),
        }

        response = client.patch(f"/vacation/{vacation.id}", json=payload)
        assert response.status_code == 422

class TestVacationDeleteEndpoints:
    def test_delete_nominal(self, client, session):
        vacation = VacationFactory(session).create()

        response = client.delete(f"/vacation/{vacation.id}")
        assert response.status_code == 204
    
    def test_idempotent(self, client, session):
        response = client.delete(f"/vacation/{uuid.uuid4()}")
        assert response.status_code == 204