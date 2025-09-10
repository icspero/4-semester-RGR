from fastapi import FastAPI, Depends, HTTPException, status, Body, Request, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import models, schemas, crud, auth
from auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
import logging
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload
from typing import List
from math import ceil
from schemas import AccessLogResponse

app = FastAPI() # объект приложения

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()
@router.get("/me/")
def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: models.Staff = Depends(get_current_user)
):
    user = db.query(models.Staff).filter(models.Staff.staff_id == current_user.staff_id).first()
    return {
        "staff_id": user.staff_id,
        "login": user.login,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "role": {
            "role_id": user.role.role_id,
            "name": user.role.name
        }
    }
app.include_router(router)

# ЛОГИРОВАНИЕ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"), # сохраняем в файл
        logging.StreamHandler() # дублируем в консоль
    ]
)

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # логируем подробности ошибки на сервере
    logger.error(f"Ошибка: {repr(exc)} | Путь: {request.url.path}")

    # возвращаем понятный ответ
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера. Мы уже работаем над этим!"}
    )



# АУТЕНТИФИКАЦИЯ
# Регистрация нового пользователя
@app.post("/register/", response_model=schemas.StaffResponse, status_code=201)
def register_user(user: schemas.StaffCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_staff_by_login(db, login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
    new_user = crud.create_staff(db, user)
    return new_user

# Вход пользователя и получение JWT
@app.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_staff_by_login(db, login=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={
            "sub": str(user.staff_id),
            "role": user.role.name
        },
        expires_delta=access_token_expires
    )

    refresh_token = auth.create_refresh_token(data={"sub": str(user.staff_id)})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.post("/refresh/")
def refresh_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен обновления",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_staff_by_id(db, staff_id=int(user_id))
    if user is None:
        raise credentials_exception

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = auth.create_access_token(
        data={
            "sub": str(user.staff_id),
            "role": user.role.name
        },
        expires_delta=access_token_expires
    )

    return {"access_token": new_access_token, "token_type": "bearer"}



# ЭНДПОИНТЫ
# Patient
@app.post("/patients/", response_model=schemas.PatientResponse, status_code=201)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    return crud.create_patient(db, patient)

from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta

@app.get("/patients/{patient_id}", response_model=schemas.PatientWithLatestCard)
def get_patient_with_latest_card(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: models.Staff = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(models.Patient.visitor_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    latest_card = (
        db.query(models.MedicalCard)
        .filter(models.MedicalCard.patient_id == patient_id)
        .order_by(models.MedicalCard.created_at.desc())
        .first()
    )

    if latest_card:
        existing_log = db.query(models.AccessLog).filter(
            models.AccessLog.doctor_id == current_user.staff_id,
            models.AccessLog.card_id == latest_card.card_id
        ).order_by(models.AccessLog.access_time.desc()).first()

        if not existing_log or (datetime.utcnow() - existing_log.access_time).total_seconds() > 1:
            crud.create_access_log(db, schemas.AccessLogCreate(
                doctor_id=current_user.staff_id,
                card_id=latest_card.card_id,
                access_type="view"
            ))

    return {
        "visitor_id": patient.visitor_id,
        "full_name": patient.full_name,
        "phone_number": patient.phone_number,
        "latest_card": {
            "diagnosis": latest_card.diagnosis if latest_card else None,
            "treatment_plan": latest_card.treatment_plan if latest_card else None,
        },
    }

@app.get("/patients/", response_model=list[schemas.PatientResponse])
def read_patients(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    db_patient = crud.update_patient(db, patient_id, patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.delete("/patients/{patient_id}", status_code=204)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    success = crud.delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"ok": True}


# Role
@app.post("/roles/", response_model=schemas.RoleResponse, status_code=201)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@app.get("/roles/{role_id}", response_model=schemas.RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.get_role(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@app.get("/roles/", response_model=list[schemas.RoleResponse])
def read_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)

@app.put("/roles/{role_id}", response_model=schemas.RoleResponse)
def update_role(role_id: int, role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.update_role(db, role_id, role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@app.delete("/roles/{role_id}", status_code=204)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    success = crud.delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"ok": True}


# Staff
@app.post("/staff/", response_model=schemas.StaffResponse, status_code=201)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db, staff)

@app.get("/staff/{staff_id}", response_model=schemas.StaffResponse)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@app.get("/staff/", response_model=list[schemas.StaffResponse])
def read_staff_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_staff_list(db, skip=skip, limit=limit)

@app.put("/staff/{staff_id}", response_model=schemas.StaffResponse)
def update_staff(staff_id: int, staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_staff = crud.update_staff(db, staff_id, staff)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@app.delete("/staff/{staff_id}", status_code=204)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    success = crud.delete_staff(db, staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"ok": True}


# MedicalCard
@app.post("/cards/", response_model=schemas.MedicalCardResponse, status_code=201)
def create_card(card: schemas.MedicalCardCreate, db: Session = Depends(get_db)):
    return crud.create_medical_card(db, card)

@app.get("/cards/{card_id}", response_model=schemas.MedicalCardResponse)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_medical_card(db, card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="MedicalCard not found")
    return db_card

@app.get("/cards/", response_model=list[schemas.MedicalCardResponse])
def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_medical_cards(db, skip=skip, limit=limit)

@app.put("/cards/{card_id}", response_model=schemas.MedicalCardResponse)
def update_card(card_id: int, card: schemas.MedicalCardCreate, db: Session = Depends(get_db)):
    db_card = crud.update_medical_card(db, card_id, card)
    if db_card is None:
        raise HTTPException(status_code=404, detail="MedicalCard not found")
    return db_card

@app.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    success = crud.delete_medical_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="MedicalCard not found")
    return {"ok": True}


# DoctorPatient
@app.get(
    "/doctorpatient/by-doctor/{doctor_id}",
    response_model=List[schemas.DoctorPatientWithLatestCardResponse]
)
def get_patients_by_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: models.Staff = Depends(get_current_user)  # проверка авторизации
):
    doctor_patients = db.query(models.DoctorPatient)\
        .options(
            joinedload(models.DoctorPatient.patient)
            .joinedload(models.Patient.medical_cards)
        )\
        .filter(models.DoctorPatient.doctor_id == doctor_id)\
        .all()

    result = []
    for dp in doctor_patients:
        patient = dp.patient
        latest_card = max(patient.medical_cards, key=lambda c: c.created_at, default=None)
        patient_data = schemas.PatientWithLatestCard(
            visitor_id=patient.visitor_id,
            full_name=patient.full_name,
            phone_number=patient.phone_number,
            latest_card=schemas.LatestCard(
                diagnosis=latest_card.diagnosis,
                treatment_plan=latest_card.treatment_plan
            ) if latest_card else None
        )
        result.append(schemas.DoctorPatientWithLatestCardResponse(
            doctor_id=dp.doctor_id,
            patient=patient_data
        ))

    return result

@app.post("/doctorpatient/", response_model=schemas.DoctorPatientResponse, status_code=201)
def create_doctor_patient(dp: schemas.DoctorPatientCreate, db: Session = Depends(get_db)):
    return crud.create_doctor_patient(db, dp)

@app.get("/doctorpatient/{doctor_id}/{patient_id}", response_model=schemas.DoctorPatientResponse)
def read_doctor_patient(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    db_dp = crud.get_doctor_patient(db, doctor_id, patient_id)
    if db_dp is None:
        raise HTTPException(status_code=404, detail="DoctorPatient not found")
    return db_dp

@app.get("/doctorpatient/", response_model=list[schemas.DoctorPatientResponse])
def read_doctor_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_doctor_patients(db, skip=skip, limit=limit)

@app.put("/doctorpatient/{doctor_id}/{patient_id}", response_model=schemas.DoctorPatientResponse)
def update_doctor_patient(doctor_id: int, patient_id: int, dp: schemas.DoctorPatientCreate, db: Session = Depends(get_db)):
    db_dp = crud.update_doctor_patient(db, doctor_id, patient_id, dp)
    if db_dp is None:
        raise HTTPException(status_code=404, detail="DoctorPatient not found")
    return db_dp

@app.delete("/doctorpatient/{doctor_id}/{patient_id}", status_code=204)
def delete_doctor_patient(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    success = crud.delete_doctor_patient(db, doctor_id, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="DoctorPatient not found")
    return {"ok": True}


# AccessLog
@app.post("/accesslog/", response_model=schemas.AccessLogResponse, status_code=201)
def create_access_log(log: schemas.AccessLogCreate, db: Session = Depends(get_db)):
    return crud.create_access_log(db, log)

@app.get("/accesslog/{log_id}", response_model=schemas.AccessLogResponse)
def read_access_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_access_log(db, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="AccessLog not found")
    return db_log

@app.get("/accesslog/")
def get_access_logs(
    page: int = 1,
    size: int = 5,
    db: Session = Depends(get_db)
):
    total_logs = db.query(models.AccessLog).count()
    total_pages = ceil(total_logs / size)

    logs = (
        db.query(models.AccessLog)
        .order_by(models.AccessLog.access_time.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    result = []
    for log in logs:
        doctor = db.query(models.Staff).filter(models.Staff.staff_id == log.doctor_id).first()
        result.append(
            AccessLogResponse(
                log_id=log.log_id,
                doctor_id=log.doctor_id,
                doctor_name=f"{doctor.first_name} {doctor.last_name}" if doctor else "Неизвестно",
                card_id=log.card_id,
                access_type=log.access_type,
                access_time=log.access_time
            )
        )

    return {
        "logs": result,
        "total_pages": total_pages,
        "current_page": page
    }

@app.put("/accesslog/{log_id}", response_model=schemas.AccessLogResponse)
def update_access_log(log_id: int, log: schemas.AccessLogCreate, db: Session = Depends(get_db)):
    db_log = crud.update_access_log(db, log_id, log)
    if db_log is None:
        raise HTTPException(status_code=404, detail="AccessLog not found")
    return db_log

@app.delete("/accesslog/{log_id}", status_code=204)
def delete_access_log(log_id: int, db: Session = Depends(get_db)):
    success = crud.delete_access_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="AccessLog not found")
    return {"ok": True}