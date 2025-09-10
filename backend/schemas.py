from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LatestCard(BaseModel):
    diagnosis: Optional[str]
    treatment_plan: Optional[str]

class PatientWithLatestCard(BaseModel):
    visitor_id: int
    full_name: str
    phone_number: Optional[str]
    latest_card: Optional[LatestCard]

class DoctorPatientWithLatestCardResponse(BaseModel):
    doctor_id: int
    patient: PatientWithLatestCard

# Role
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    role_id: int

    class Config:
        orm_mode = True


# Staff
class StaffBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    phone_number: str
    login: str
    role_id: int

class StaffCreate(StaffBase):
    password: str  # при создании добавляем пароль

class StaffResponse(StaffBase):
    staff_id: int

    class Config:
        orm_mode = True


# Patient
class PatientBase(BaseModel):
    full_name: str
    phone_number: str
    is_patient: bool

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    visitor_id: int
    date_registration: datetime

    class Config:
        orm_mode = True


# MedicalCard
class MedicalCardBase(BaseModel):
    patient_id: int
    diagnosis: str
    treatment_plan: str

class MedicalCardCreate(MedicalCardBase):
    pass

class MedicalCardResponse(MedicalCardBase):
    card_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DoctorPatientBase(BaseModel):
    doctor_id: int
    patient_id: int

class DoctorPatientCreate(DoctorPatientBase):
    pass

class DoctorPatientResponse(DoctorPatientBase):
    class Config:
        orm_mode = True


# AccessLog
class AccessLogBase(BaseModel):
    doctor_id: int
    card_id: int
    access_type: str

class AccessLogCreate(AccessLogBase):
    pass

class AccessLogResponse(BaseModel):
    log_id: int
    doctor_id: int
    doctor_name: Optional[str]
    card_id: int
    access_type: str
    access_time: datetime

    class Config:
        orm_mode = True