import os
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from clinic.models import Doctor, Patient
from clinic.service import ClinicService


app = FastAPI(title="Сервіс записів і відвідувань")
clinic = ClinicService()
REGISTRY_URL = os.getenv("REGISTRY_URL", "http://127.0.0.1:8001")


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    starts_at: datetime


def load_from_registry(path: str) -> dict:
    try:
        response = httpx.get(f"{REGISTRY_URL}{path}", timeout=3.0)
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail="Сервіс лікарів і пацієнтів недоступний",
        ) from error

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Лікаря або пацієнта не знайдено")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Помилка сервісу лікарів і пацієнтів")

    return response.json()


@app.post("/appointments", status_code=201)
def book_appointment(data: AppointmentCreate):
    doctor_data = load_from_registry(f"/doctors/{data.doctor_id}")
    patient_data = load_from_registry(f"/patients/{data.patient_id}")

    clinic.doctors[data.doctor_id] = Doctor(**doctor_data)
    clinic.patients[data.patient_id] = Patient(**patient_data)

    try:
        return clinic.book_appointment(
            data.doctor_id, data.patient_id, data.starts_at
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int):
    appointment = clinic.appointments.get(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return appointment


@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    if appointment_id not in clinic.appointments:
        raise HTTPException(status_code=404, detail="Запис не знайдено")

    try:
        return clinic.complete_appointment(appointment_id)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error