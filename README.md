# FastAPI_demo

# 🏥 Patient Management API using FastAPI

This is a simple and fully functional  **FastAPI** for managing patient health records. The application allows you to **create**, **view**, **edit**, **delete**, and **sort** patient data — all while automatically calculating their **BMI (Body Mass Index)** and assigning a **health verdict** like *Underweight*, *Normal*, *Overweight*, or *Obese*.



##  What this project does

- Stores patient details in a local JSON file (`patient.json`)
- Calculates BMI automatically from height and weight
- Gives a health verdict based on BMI value
- Allows CRUD operations on patient data
- Sorts patients based on height or weight
- Validates all input using FastAPI & Pydantic


**ALL the required steps to run locally**
###
-1. Clone the Repository
-2. Create a Virtual Environment
   python -m venv venv
   source venv/bin/activate      # On macOS/Linux
   venv\Scripts\activate         # On Windows

-3.Install the Dependencies
pip install -r requirements.txt
-4.Run the API
uvicorn main:app --reload



**About Endpoint**
- GET `/` – Returns a welcome message  
- GET `/about` – About the application  
- GET `/view` – View all patients  
- GET `/view/{id}` – View a specific patient by ID  
- GET `/sort?sort_by=height&order=asc` – Sort patients by height or weight  
- POST `/create` – Create a new patient  
- PUT `/edit/{id}` – Edit a patient's details  
- DELETE `/delete/{id}` – Delete a patient by ID  

