import json
from app.db.database import Session, engine
from app.models.patient import Base, Patient


def seed_database() -> None:
    with open("patients.json", encoding="utf-8") as file:
        patients = json.load(file)

    Base.metadata.create_all(bind=engine)
    db = Session()

    try:
        for patient_id, patient_data in patients.items():
            db.merge(
                Patient(
                    id=patient_id,
                    name=patient_data["name"],
                    age=patient_data["age"],
                    gender=patient_data["gender"].lower(),
                    height=patient_data["height"],
                    weight=patient_data["weight"],
                    diagnosis=patient_data["diagnosis"],
                    last_visit=patient_data["last_visit"],
                )
            )

        db.commit()
        print(f"Seeded {len(patients)} patients into MySQL.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()