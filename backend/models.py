from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CHAR, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Role(Base):
    __tablename__ = "role"
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    staff_members = relationship("Staff", back_populates="role")


class Staff(Base):
    __tablename__ = "staff"
    staff_id = Column(Integer, primary_key=True, index=True)
    last_name = Column(CHAR(30), nullable=False)
    first_name = Column(CHAR(30), nullable=False)
    middle_name = Column(CHAR(30), nullable=True)
    phone_number = Column(CHAR(30), nullable=False)
    login = Column(CHAR(30), nullable=False, unique=True)
    password = Column(CHAR(100), nullable=False)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)

    role = relationship("Role", back_populates="staff_members")
    doctor_patients = relationship("DoctorPatient", back_populates="doctor")
    access_logs = relationship("AccessLog", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patient"
    visitor_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(CHAR(100), nullable=False)
    phone_number = Column(CHAR(30), nullable=False)
    is_patient = Column(Boolean, nullable=False)
    date_registration = Column(DateTime, default=datetime.utcnow, nullable=False)

    medical_cards = relationship("MedicalCard", back_populates="patient")
    doctor_patients = relationship("DoctorPatient", back_populates="patient")


class MedicalCard(Base):
    __tablename__ = "medicalcard"
    card_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.visitor_id"), nullable=False)
    diagnosis = Column(CHAR(200), nullable=False)
    treatment_plan = Column(CHAR(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    patient = relationship("Patient", back_populates="medical_cards")
    access_logs = relationship("AccessLog", back_populates="medical_card")


class DoctorPatient(Base):
    __tablename__ = "doctorpatient"
    doctor_id = Column(Integer, ForeignKey("staff.staff_id"), primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.visitor_id"), primary_key=True)

    doctor = relationship("Staff", back_populates="doctor_patients")
    patient = relationship("Patient", back_populates="doctor_patients")


class AccessLog(Base):
    __tablename__ = "accesslog"
    log_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("medicalcard.card_id"), nullable=False)
    access_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    access_type = Column(CHAR(20), nullable=False)

    doctor = relationship("Staff", back_populates="access_logs")
    medical_card = relationship("MedicalCard", back_populates="access_logs")

    __table_args__ = (
        UniqueConstraint("doctor_id", "card_id", "access_type", name="unique_access_log"),
    )