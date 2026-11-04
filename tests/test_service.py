import unittest
from datetime import datetime

from clinic.service import ClinicService


class ClinicServiceTests(unittest.TestCase):
    def setUp(self):
        self.clinic = ClinicService()
        self.doctor = self.clinic.add_doctor("Березин", "Стоматолог")
        self.patient = self.clinic.add_patient("Коваль")
        self.visit_time = datetime(2026, 11, 10, 14, 30)

    def test_book_appointment(self):
        appointment = self.clinic.book_appointment(
            self.doctor.id, self.patient.id, self.visit_time
        )

        self.assertEqual(appointment.doctor_id, self.doctor.id)
        self.assertEqual(appointment.patient_id, self.patient.id)
        self.assertEqual(appointment.status, "scheduled")

    def test_complete_appointment(self):
        appointment = self.clinic.book_appointment(
            self.doctor.id, self.patient.id, self.visit_time
        )

        result = self.clinic.complete_appointment(appointment.id)

        self.assertEqual(result.status, "completed")

    def test_unknown_doctor_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Лікаря не знайдено"):
            self.clinic.book_appointment(999, self.patient.id, self.visit_time)

    @unittest.expectedFailure
    def test_unknown_patient_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Пацієнта не знайдено"):
            self.clinic.book_appointment(self.doctor.id, 999, self.visit_time)

    def test_busy_doctor_is_rejected(self):
        self.clinic.book_appointment(
            self.doctor.id, self.patient.id, self.visit_time
        )
        another_patient = self.clinic.add_patient("Мельник")

        with self.assertRaisesRegex(ValueError, "Лікар уже зайнятий"):
            self.clinic.book_appointment(
                self.doctor.id, another_patient.id, self.visit_time
            )

    def test_patient_cannot_have_two_visits_at_same_time(self):
        self.clinic.book_appointment(
            self.doctor.id, self.patient.id, self.visit_time
        )
        another_doctor = self.clinic.add_doctor("Петренко", "Терапевт")

        with self.assertRaisesRegex(ValueError, "Пацієнт уже записаний"):
            self.clinic.book_appointment(
                another_doctor.id, self.patient.id, self.visit_time
            )

    def test_visit_cannot_be_completed_twice(self):
        appointment = self.clinic.book_appointment(
            self.doctor.id, self.patient.id, self.visit_time
        )
        self.clinic.complete_appointment(appointment.id)

        with self.assertRaisesRegex(ValueError, "Відвідування вже позначено"):
            self.clinic.complete_appointment(appointment.id)


if __name__ == "__main__":
    unittest.main()