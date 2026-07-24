from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Employee Information API")


# Employee Model
class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


# Sample Data
employees = [
    {"id": 1, "name": "Alice", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Bob", "department": "IT", "salary": 70000},
    {"id": 3, "name": "Charlie", "department": "Finance", "salary": 65000},
]


# 1. Home Route
@app.get("/")
def home():
    return {"message": "Employee Information API"}


# 2. Get All Employees
@app.get("/employees")
def get_employees():
    return employees


# 3. Get Employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


# 4. Add New Employee
@app.post("/employees")
def add_employee(employee: Employee):
    for emp in employees:
        if emp["id"] == employee.id:
            raise HTTPException(status_code=400, detail="Employee ID already exists")

    employees.append(employee.dict())
    return {
        "message": "Employee added successfully",
        "employee": employee
    }


# 5. Search Employees by Department
@app.get("/search")
def search_employees(department: str):
    result = [
        emp for emp in employees
        if emp["department"].lower() == department.lower()
    ]
    return result


# 6. Custom Response
@app.get("/application-info")
def application_info():
    return JSONResponse(
        status_code=200,
        content={
            "application": "Employee Information API",
            "version": "1.0",
            "developer": "Your Name"
        }
    )
