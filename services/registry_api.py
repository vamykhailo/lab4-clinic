from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from clinic.service import ClinicService


app = FastAPI(title="Сервіс лікарів і пацієнтів")
clinic = ClinicService()


class DoctorCreate(BaseModel):
    full_name: str
    specialty: str


class PatientCreate(BaseModel):
    full_name: str


@app.post("/doctors", status_code=201)
def add_doctor(data: DoctorCreate):
    try:
        return clinic.add_doctor(data.full_name, data.specialty)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = clinic.doctors.get(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Лікаря не знайдено")
    return doctor


@app.post("/patients", status_code=201)
def add_patient(data: PatientCreate):
    try:
        return clinic.add_patient(data.full_name)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patient = clinic.patients.get(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Пацієнта не знайдено")
    return patient