from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
from passlib.context import CryptContext

# ===== Настройка хэширования паролей =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ===== Role =====
def get_roles(db: Session):
    return db.query(models.Role).all()

def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.role_id == role_id).first()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_data: schemas.RoleCreate):
    role = get_role(db, role_id)
    if role:
        for key, value in role_data.dict().items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if role:
        db.delete(role)
        db.commit()
        return True
    return False


# ===== Staff =====
def get_staff(db: Session):
    return db.query(models.Staff).all()

def get_staff_by_id(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.staff_id == staff_id).first()

def get_staff_by_login(db: Session, login: str):
    return db.query(models.Staff).filter(models.Staff.login == login).first()

def create_staff(db: Session, staff: schemas.StaffCreate):
    hashed_password = get_password_hash(staff.password)
    db_staff = models.Staff(**staff.dict(exclude={"password"}), password=hashed_password)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def update_staff(db: Session, staff_id: int, staff_data: schemas.StaffCreate):
    staff = get_staff_by_id(db, staff_id)
    if staff:
        for key, value in staff_data.dict(exclude={"password"}).items():
            setattr(staff, key, value)
        # Если передан новый пароль, обновляем хэш
        if staff_data.password:
            staff.password = get_password_hash(staff_data.password)
        db.commit()
        db.refresh(staff)
    return staff

def delete_staff(db: Session, staff_id: int):
    staff = get_staff_by_id(db, staff_id)
    if staff:
        db.delete(staff)
        db.commit()
        return True
    return False


# ===== Patient =====
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.visitor_id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db_patient = db.query(models.Patient).filter(models.Patient.visitor_id == patient_id).first()
    if db_patient is None:
        return None
    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(models.Patient).filter(models.Patient.visitor_id == patient_id).first()
    if db_patient is None:
        return False
    db.delete(db_patient)
    db.commit()
    return True


# ===== MedicalCard =====
def get_medical_cards(db: Session):
    return db.query(models.MedicalCard).all()

def get_medical_card(db: Session, card_id: int):
    return db.query(models.MedicalCard).filter(models.MedicalCard.card_id == card_id).first()

def create_medical_card(db: Session, card: schemas.MedicalCardCreate):
    db_card = models.MedicalCard(**card.dict(), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_medical_card(db: Session, card_id: int, card_data: schemas.MedicalCardCreate):
    card = get_medical_card(db, card_id)
    if card:
        for key, value in card_data.dict().items():
            setattr(card, key, value)
        card.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(card)
    return card

def delete_medical_card(db: Session, card_id: int):
    card = get_medical_card(db, card_id)
    if card:
        db.delete(card)
        db.commit()
        return True
    return False


# ===== DoctorPatient =====
def get_doctor_patients(db: Session):
    return db.query(models.DoctorPatient).all()

def create_doctor_patient(db: Session, dp: schemas.DoctorPatientCreate):
    db_dp = models.DoctorPatient(**dp.dict())
    db.add(db_dp)
    db.commit()
    db.refresh(db_dp)
    return db_dp

def delete_doctor_patient(db: Session, doctor_id: int, patient_id: int):
    dp = db.query(models.DoctorPatient).filter(
        models.DoctorPatient.doctor_id == doctor_id,
        models.DoctorPatient.patient_id == patient_id
    ).first()
    if dp:
        db.delete(dp)
        db.commit()
        return True
    return False

def get_doctor_patient(db: Session, doctor_id: int, patient_id: int):
    return db.query(models.DoctorPatient).filter(
        models.DoctorPatient.doctor_id == doctor_id,
        models.DoctorPatient.patient_id == patient_id
    ).first()

def update_doctor_patient(db: Session, doctor_id: int, patient_id: int, dp_data: schemas.DoctorPatientCreate):
    dp = get_doctor_patient(db, doctor_id, patient_id)
    if dp:
        for key, value in dp_data.dict().items():
            setattr(dp, key, value)
        db.commit()
        db.refresh(dp)
    return dp



# ===== AccessLog =====
def get_access_logs(db: Session):
    return db.query(models.AccessLog).all()

def create_access_log(db: Session, log: schemas.AccessLogCreate):
    db_log = models.AccessLog(**log.dict(), access_time=datetime.utcnow())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_access_log(db: Session, log_id: int):
    return db.query(models.AccessLog).filter(models.AccessLog.log_id == log_id).first()

def update_access_log(db: Session, log_id: int, log_data: schemas.AccessLogCreate):
    log = get_access_log(db, log_id)
    if log:
        for key, value in log_data.dict().items():
            setattr(log, key, value)
        log.access_time = datetime.utcnow()
        db.commit()
        db.refresh(log)
    return log

def delete_access_log(db: Session, log_id: int):
    log = get_access_log(db, log_id)
    if log:
        db.delete(log)
        db.commit()
        return True
    return False
