from fastapi import FastAPI
import json
from pydantic import BaseModel,computed_field,Field
from typing import Annotated,Literal
from typing import List,Optional
from fastapi import HTTPException,Query
from fastapi.responses import JSONResponse
# pydantic model 
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Unique identifier for the patient',examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male','female','others'], Field(..., description=' Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]  #... means required parameter
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]  

    @computed_field
    @property
    def bmi(self) -> float:
        if self.height <= 0:
            return 0.0
        return round(self.weight / (self.height ** 2), 2)
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description='Name of the patient')]
    city: Annotated[Optional[str], Field(default=None, description='City of the patient')]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None, description='Gender of the patient')]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight of the patient in kg")]


def load_data():
    with open('patient.json', 'r') as file:
        data= json.load(file)
    return data

def save_data(data):
    with open('patient.json', 'w') as file:
        json.dump(data, file)

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get('/about')
def about():
    return {"message": "This is a simple FastAPI application."} 

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/view/{id}')
def view_patient(id: str):
    data=load_data()
    if id in data:
        return data[id]
    raise HTTPException(status_code=404, detail="Patient not found")
  # receiving data

@app.get('/sort')
# ... means required parameter
def sort_patients(sort_by: str=Query(...,description="Sort by 'height' "), order: str = Query('asc', description="Order of sorting, 'asc' or 'desc'")):
    valid_fields = ['height', 'weight']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    data= load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse= False if order == 'asc' else True)
    return sorted_data 



@app.post('/create')
def create_patient(patient: Patient): # if we receive data in json format, we can use pydantic model to validate it
    # Load existing data when we call load_data so already existing data will be loaded in data variable
    data = load_data()

    # Check if patient with the same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    #new patient data will be added to the existing data
    data[patient.id]=patient.model_dump(exclude=['id'])  # Convert Pydantic model to dict   
    # when new patient data is coming , bmi and verdict will be calculated automatically because of the computed fields

    # Save updated data back to the file
    save_data(data)
    return JSONResponse(status_code=201,content={"message": "Patient created successfully", "patient": data[patient.id]}) 


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update only provided fields
    for key, value in patient_update.model_dump(exclude_unset=True).items():
        data[patient_id][key] = value

    # Recalculate bmi and verdict using Patient model
#     It creates a new Patient object using the updated data.
# This automatically recalculates bmi and verdict using your computed properties.
    updated_patient = Patient(id=patient_id, **data[patient_id])
    data[patient_id] = updated_patient.model_dump(exclude=['id'])
    save_data(data)
    return {"message": "Patient updated successfully", "patient": data[patient_id]}


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):    
    data = load_data()

    # Check if patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Delete the patient from the data
    del data[patient_id]

    # Save updated data back to the file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})   
