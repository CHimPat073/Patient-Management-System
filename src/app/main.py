from fastapi import Depends, FastAPI, HTTPException, Query
from app.schemas.patient import Patient
from app.db.database import engine, get_db
import app.models.patient as patient
from datetime import datetime
from app.routers.patients import router as patients_router


app=FastAPI()

app.include_router(patients_router)

patient.Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return {'message': "patients Management system API"}

@app.get("/about")
def about():
    return {'message': "A fully functional patients management system API built with FastAPI."}




@app.get('/sort', summary='Sort patients', description='Sort all patients by age or last visit date in ascending or descending order.')
def sort_patient(
    sort_by: str = Query(..., description='Field to sort by: age or last_visit'),
    order: str = Query('asc', description='Sort order: asc for ascending or desc for descending'),
    db=Depends(get_db)
):
    valid_fields = ['age', 'last_visit']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Valid fields: {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

    patients = db.query(patient.Patient).all()

    if sort_by == 'age':
        sorted_patients = sorted(patients, key=lambda p: p.age, reverse=(order == "desc"))
    else:
        sorted_patients = sorted(
            patients,
            key=lambda p: datetime.strptime(str(p.last_visit), "%Y-%m-%d").date(),
            reverse=(order == "desc")
        )

    return [Patient.model_validate(p).model_dump() for p in sorted_patients]
