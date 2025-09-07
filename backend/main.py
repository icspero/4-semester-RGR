from fastapi import FastAPI, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import models, schemas, crud, auth
from auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

# ====== Настройка логирования ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # сохраняем в файл
        logging.StreamHandler()          # дублируем в консоль
    ]
)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # логируем подробности ошибки на сервере
    logger.error(f"Ошибка: {repr(exc)} | Путь: {request.url.path}")

    # возвращаем пользователю понятный ответ
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера. Мы уже работаем над этим!"}
    )



# ========== АУТЕНТИФИКАЦИЯ ==========
# --------------------
# Регистрация нового пользователя
# --------------------
@app.post("/register/", response_model=schemas.StaffResponse, status_code=201)
def register_user(user: schemas.StaffCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_staff_by_login(db, login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
    new_user = crud.create_staff(db, user)
    return new_user


# --------------------
# Вход пользователя и получение JWT
# --------------------
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
        data={"sub": str(user.staff_id)},
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
        data={"sub": str(user.staff_id)}, expires_delta=access_token_expires
    )

    return {"access_token": new_access_token, "token_type": "bearer"}

# ========== ПРИМЕР ЗАЩИЩЁННЫХ ЭНДПОИНТОВ ==========


# --------------------
# CRUD для Patient
# --------------------

@app.post("/patients/", response_model=schemas.PatientResponse, status_code=201)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    return crud.create_patient(db, patient)

@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.StaffResponse = Depends(get_current_user)
):
    db_patient = crud.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

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


# --------------------
# CRUD для Role
# --------------------
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


# --------------------
# CRUD для Staff
# --------------------
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

# --------------------
# CRUD для MedicalCard
# --------------------
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


# --------------------
# CRUD для DoctorPatient
# --------------------
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


# --------------------
# CRUD для AccessLog
# --------------------
@app.post("/accesslog/", response_model=schemas.AccessLogResponse, status_code=201)
def create_access_log(log: schemas.AccessLogCreate, db: Session = Depends(get_db)):
    return crud.create_access_log(db, log)

@app.get("/accesslog/{log_id}", response_model=schemas.AccessLogResponse)
def read_access_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_access_log(db, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="AccessLog not found")
    return db_log

@app.get("/accesslog/", response_model=list[schemas.AccessLogResponse])
def read_access_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_access_logs(db, skip=skip, limit=limit)

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