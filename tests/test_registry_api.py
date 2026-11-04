import unittest

from fastapi.testclient import TestClient

from clinic.service import ClinicService
from services import registry_api


class RegistryApiTests(unittest.TestCase):
    def setUp(self):
        registry_api.clinic = ClinicService()
        self.client = TestClient(registry_api.app)

    def test_create_and_get_doctor(self):
        created = self.client.post(
            "/doctors",
            json={"full_name": "Березин", "specialty": "Стоматолог"},
        )

        self.assertEqual(created.status_code, 201)
        doctor_id = created.json()["id"]

        received = self.client.get(f"/doctors/{doctor_id}")
        self.assertEqual(received.status_code, 200)
        self.assertEqual(received.json()["full_name"], "Березин")

    def test_create_and_get_patient(self):
        created = self.client.post(
            "/patients",
            json={"full_name": "Коваль"},
        )

        self.assertEqual(created.status_code, 201)
        patient_id = created.json()["id"]

        received = self.client.get(f"/patients/{patient_id}")
        self.assertEqual(received.status_code, 200)
        self.assertEqual(received.json()["full_name"], "Коваль")

    def test_unknown_doctor_returns_404(self):
        response = self.client.get("/doctors/999")
        self.assertEqual(response.status_code, 404)

    def test_unknown_patient_returns_404(self):
        response = self.client.get("/patients/999")
        self.assertEqual(response.status_code, 404)

    def test_empty_doctor_name_returns_400(self):
        response = self.client.post(
            "/doctors",
            json={"full_name": "   ", "specialty": "Стоматолог"},
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()