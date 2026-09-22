from typing import Annotated,Literal,Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import date


class Patient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:Annotated[str,Field(...,description="ID of patient",examples=['P001'])]
    name:Annotated[str,Field(...,description='name Of the Patient')]
    age:Annotated[int,Field(...,gt=0,lt=100,description="age of patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="gender of patient")]
    height:Annotated[float,Field(...,description="height of pateints")]
    weight:Annotated[float,Field(...,description="weight of pateints")]
    diagnosis:Annotated[str,Field(...,description="symptoms")]
    last_visit:Annotated[date,Field(...,description="last visit date")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round((self.weight/(self.height**2)*10000),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'OverWeight'
        else:
            return 'Obesed'
    
    @computed_field
    @property
    def treatment(self) -> str:
        if self.diagnosis == "Hypertension":
            return "Medication"
        elif self.diagnosis == "Diabetes":
            return "Insulin Therapy"
        elif self.diagnosis == "Asthma":
            return "Inhaler"
        elif self.diagnosis == "Arthritis":
            return "Physical Therapy"
        elif self.diagnosis == "Depression":
            return "Counseling"
        else:
            return "Consult Doctor"

class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
    diagnosis:Annotated[Optional[str],Field(default=None)]
    last_visit:Annotated[Optional[str],Field(default=None)]
