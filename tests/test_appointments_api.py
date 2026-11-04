import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from clinic.service import ClinicService
from services import appointments_api


class AppointmentsApiTests(unittest.TestCase):
    def setUp(self):
        appointments_api.clinic = ClinicService()
        self.client = TestClient(appointments_api.app)
        self.data = {
            "doctor_id": 1,
            "patient_id": 1,
            "starts_at": "2026-11-10T14:30:00",
        }

    @staticmethod
    def registry_response(url, timeout):
        if url.endswith("/doctors/1"):
            return httpx.Response(
                200,
                json={"id": 1, "full_name": "Березин", "specialty": "Стоматолог"},
            )
        if url.endswith("/patients/1"):
            return httpx.Response(
                200,
                json={"id": 1, "full_name": "Коваль"},
            )
        if url.endswith("/patients/2"):
            return httpx.Response(
                200,
                json={"id": 2, "full_name": "Мельник"},
            )
        return httpx.Response(404, json={"detail": "Не знайдено"})

    def test_create_and_get_appointment(self):
        with patch(
            "services.appointments_api.httpx.get",
            side_effect=self.registry_response,
        ):
            created = self.client.post("/appointments", json=self.data)

        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["status"], "scheduled")

        appointment_id = created.json()["id"]
        received = self.client.get(f"/appointments/{appointment_id}")
        self.assertEqual(received.status_code, 200)
        self.assertEqual(received.json()["doctor_id"], 1)

    def test_complete_appointment_and_reject_repeated_completion(self):
        with patch(
            "services.appointments_api.httpx.get",
            side_effect=self.registry_response,
        ):
            created = self.client.post("/appointments", json=self.data)

        appointment_id = created.json()["id"]
        completed = self.client.post(f"/appointments/{appointment_id}/complete")
        repeated = self.client.post(f"/appointments/{appointment_id}/complete")

        self.assertEqual(completed.status_code, 200)
        self.assertEqual(completed.json()["status"], "completed")
        self.assertEqual(repeated.status_code, 409)

    def test_unknown_doctor_returns_404(self):
        data = {**self.data, "doctor_id": 999}

        with patch(
            "services.appointments_api.httpx.get",
            side_effect=self.registry_response,
        ):
            response = self.client.post("/appointments", json=data)

        self.assertEqual(response.status_code, 404)

    def test_busy_doctor_returns_409(self):
        with patch(
            "services.appointments_api.httpx.get",
            side_effect=self.registry_response,
        ):
            first = self.client.post("/appointments", json=self.data)
            second = self.client.post(
                "/appointments",
                json={**self.data, "patient_id": 2},
            )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_unavailable_registry_returns_503(self):
        with patch(
            "services.appointments_api.httpx.get",
            side_effect=httpx.ConnectError("Сервіс недоступний"),
        ):
            response = self.client.post("/appointments", json=self.data)

        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()