from fastapi import APIRouter, Depends, Path, HTTPException, Query
from app.db.database import get_db
from app.models.patient import Patient as PatientModel
from app.repositories.patient_repository import (
    delete_patient as delete_patient_record,
    get_all_patients,
    get_patient_by_id,
    save_patient,
    update_patient as update_patient_record,
)
from app.schemas.patient import Patient, PatientUpdate

router = APIRouter(prefix='/patients', tags=['patients'])

@router.get('', response_model=list[Patient])
def view_patients(db=Depends(get_db)):
    patients = get_all_patients(db)
    return [Patient.model_validate(patient).model_dump() for patient in patients]

@router.get('/{patient_id}', response_model=Patient)
def view_patient(
    patient_id: str = Path(..., description='ID of the patient in the DB', examples='P001'),
    db=Depends(get_db),
):
    patient = get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(status_code=404, detail='Patient Not found')

    return Patient.model_validate(patient).model_dump()

@router.post('', status_code=201)
def create_patient(patient: Patient, db=Depends(get_db)):
    #load existing data
    # data=load_data()
    existing_patient = get_patient_by_id(db, patient.id)
    #check if the pateient already exits
    if existing_patient is not None:
        raise HTTPException(status_code=409, detail='Patient already exists')
    #new patient add
    new_data = PatientModel(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight,
        diagnosis=patient.diagnosis,
        last_visit=patient.last_visit,
    )
    #add to new db via patient_repository
    save_patient(db,new_data)
    #save to json
    # save_data(data)

    return {'message': 'patient created'}


@router.put('/{patient_id}')
#path param as patient id  and req body will be a obj of patient Update pydantic obj 
def update_patient(patient_id: str, patient_update: PatientUpdate, db=Depends(get_db)):
    patient = get_patient_by_id(db, patient_id)
    
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
    update_patient_record(db, patient)

    return {'message': 'patient updated'}


@router.delete('/{patient_id}')
def delete_patient(patient_id: str, db=Depends(get_db)):
    patient = get_patient_by_id(db, patient_id)
    #load data
    # data= load_data()

    if patient is None:
        raise HTTPException(status_code=404 , detail='Patient not Found')

    # del data[patient_id]
    delete_patient_record(db, patient)

    # save_data(data)

    return {'message': 'patient deleted'}
