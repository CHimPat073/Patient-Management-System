from sqlalchemy.orm import Session

from app.models.patient import Patient


def get_patient_by_id(db: Session, patient_id: str) -> Patient | None:
    return db.get(Patient, patient_id)


def get_all_patients(db: Session) -> list[Patient]:
    return db.query(Patient).all()


def add_patient(db: Session, patient: Patient) -> None:
    db.add(patient)


def commit_patient(db: Session) -> None:
    db.commit()


def refresh_patient(db: Session, patient: Patient) -> None:
    db.refresh(patient)


def update_patient(db: Session, patient: Patient) -> None:
    db.commit()
    db.refresh(patient)


def delete_patient(db: Session, patient: Patient) -> None:
    db.delete(patient)
    db.commit()


def save_patient(db: Session, patient: Patient) -> Patient:
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
