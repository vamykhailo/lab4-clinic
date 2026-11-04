from dataclasses import dataclass
from datetime import datetime


@dataclass
class Doctor:
    id: int
    full_name: str
    specialty: str


@dataclass
class Patient:
    id: int
    full_name: str


@dataclass
class Appointment:
    id: int
    doctor_id: int
    patient_id: int
    starts_at: datetime
    status: str = "scheduled"