from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

employees = [
    {"id": 1, "name": "John", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Alice", "department": "IT", "salary": 70000},
    {"id": 3, "name": "Bob", "department": "Finance", "salary": 60000}
]

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: int

@app.get("/")
def home():
    return {"message": "Employee Information API"}

@app.get("/employees")
def get_all_employees():
    return employees

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees")
def add_employee(employee: Employee):
    employees.append(employee.model_dump())
    return {"message": "Employee added successfully"}

@app.get("/search")
def search(department: str = Query(...)):
    result = [
        employee
        for employee in employees
        if employee["department"].lower() == department.lower()
    ]
    return result

@app.get("/application-info")
def application_info():
    return {
        "application": "Employee Information API",
        "version": "1.0"
    }
