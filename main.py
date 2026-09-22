from fastapi import Depends, FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from schema import Patient,PatientUpdate
from database import Session,engine
import models


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def load_data():
    with open("patients.json", "r") as f:
        data= json.load(f)
        return data
    

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

treatment_map = {
    "Hypertension": "Medication",
    "Diabetes": "Insulin Therapy",
    "Asthma": "Inhaler",
    "Arthritis": "Physical Therapy",
    "Depression": "Counseling"
}

@app.get("/")
def hello():
    return {'message': "patients Management system API"}

@app.get("/about")
def about():
    return {'message': "A fully functional patients management system API built with FastAPI."}

@app.get('/veiw')
def veiw(db=Depends(get_db)):
    patients = db.query(models.Patient).all()
    return [Patient.model_validate(patient).model_dump() for patient in patients]

@app.get('/veiw/{patient_id}')
def veiw_patient(
    patient_id: str = Path(..., description='ID of the patient in the DB', examples='P001'),
    db=Depends(get_db),
):
    patient = db.get(models.Patient, patient_id)

    if patient is None:
        raise HTTPException(status_code=404, detail='Patient Not found')

    return Patient.model_validate(patient).model_dump()


@app.get('/sort')
def sort_patient(sort_by:str=Query(...,description="Sort on basis of age,last_visit"),order:str=Query('asc',description="sort on asc or desc order"),db=Depends(get_db)):
    valid_fields=['age','last_visit']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field {valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid field.')

    data=load_data()

    sort_order= True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient:Patient,db=Depends(get_db)):
    #load existing data
    # data=load_data()
    existing_patient=db.get(models.Patient,patient.id)
    #check if the pateient already exits
    if existing_patient is not None:
        raise HTTPException(status_code=400,detail="Already exits")
    #new patient add
    new_data=models.Patient(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight,
        diagnosis=patient.diagnosis,
        last_visit=patient.last_visit,
    )
    #add to new db
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    #save to json
    # save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created'})


@app.put('/edit/{patient_id}')
#path param as patient id  and req body will be a obj of patient Update pydantic obj 
def updatepatient(patient_id:str,patient_update:PatientUpdate,db=Depends(get_db)):
    patient= db.get(models.Patient,patient_id)
    
    # data=load_data()

    if patient is None:
        raise HTTPException(status_code=404,detail='Patient not found')

    # exsitingpatient_info = data[patient_id]

    updated_data = patient_update.model_dump(exclude_unset=True)

    # setattr is a built-in Python function that sets an object attribute using a string name.
    for key ,val in updated_data.items():
        setattr(patient,key,val)

    #existing_patient_info -> Pydantic obj -> updated bmI+verdicts
    # pydantic obj ->dict
    
    # exsitingpatient_info['id'] = patient_id
    # patient_pydantic_obj = Patient(**exsitingpatient_info)

    # exsitingpatient_info = patient_pydantic_obj.model_dump(exclude='id')

    # #adding the data
    # data[patient_id] = exsitingpatient_info

    # save_data(data)
    db.commit()
    db.refresh(patient)

    return JSONResponse(status_code=200,content={'message':'patient updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id,db=Depends(get_db)):
    patient=db.get(models.Patient,patient_id)
    #load data
    # data= load_data()

    if patient is None:
        raise HTTPException(status_code=404 , detail='Patient not Found')

    # del data[patient_id]
    db.delete(patient)
    db.commit()

    # save_data(data)

    return JSONResponse(status_code=200, content="Data Deleted")