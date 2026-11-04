from datetime import datetime

from clinic.models import Appointment, Doctor, Patient


class ClinicService:
    def __init__(self):
        self.doctors: dict[int, Doctor] = {}
        self.patients: dict[int, Patient] = {}
        self.appointments: dict[int, Appointment] = {}

    def add_doctor(self, full_name: str, specialty: str) -> Doctor:
        if not full_name.strip() or not specialty.strip():
            raise ValueError("Вкажіть ім'я та спеціальність лікаря")

        doctor = Doctor(
            id=len(self.doctors) + 1,
            full_name=full_name.strip(),
            specialty=specialty.strip(),
        )
        self.doctors[doctor.id] = doctor
        return doctor

    def add_patient(self, full_name: str) -> Patient:
        if not full_name.strip():
            raise ValueError("Вкажіть ім'я пацієнта")

        patient = Patient(
            id=len(self.patients) + 1,
            full_name=full_name.strip(),
        )
        self.patients[patient.id] = patient
        return patient

    def book_appointment(
        self, doctor_id: int, patient_id: int, starts_at: datetime
    ) -> Appointment:
        if doctor_id not in self.doctors:
            raise ValueError("Лікаря не знайдено")
        if patient_id not in self.patients:
            raise ValueError("Пацієнта не знайдено")
        if not isinstance(starts_at, datetime):
            raise ValueError("Дата і час мають бути типу datetime")

        for existing in self.appointments.values():
            if existing.starts_at == starts_at and existing.status == "scheduled":
                if existing.doctor_id == doctor_id:
                    raise ValueError("Лікар уже зайнятий у цей час")
                if existing.patient_id == patient_id:
                    raise ValueError("Пацієнт уже записаний на цей час")

        appointment = Appointment(
            id=len(self.appointments) + 1,
            doctor_id=doctor_id,
            patient_id=patient_id,
            starts_at=starts_at,
        )
        self.appointments[appointment.id] = appointment
        return appointment

    def complete_appointment(self, appointment_id: int) -> Appointment:
        appointment = self.appointments.get(appointment_id)
        if appointment is None:
            raise ValueError("Запис не знайдено")
        if appointment.status != "scheduled":
            raise ValueError("Відвідування вже позначено")

        appointment.status = "completed"
        return appointment