from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Employee Information API")

# In-memory database
employees = [
    {
        "id": 1,
        "name": "Alice",
        "department": "HR",
        "designation": "Manager"
    },
    {
        "id": 2,
        "name": "Bob",
        "department": "IT",
        "designation": "Developer"
    },
    {
        "id": 3,
        "name": "Charlie",
        "department": "Finance",
        "designation": "Analyst"
    }
]


class Employee(BaseModel):
    id: int
    name: str
    department: str
    designation: str


# Home Route
@app.get("/")
def home():
    return {"application": "Employee Information API"}


# Get all employees
@app.get("/employees")
def get_employees():
    return employees


# Get employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


# Add a new employee
@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    for emp in employees:
        if emp["id"] == employee.id:
            raise HTTPException(
                status_code=400,
                detail="Employee ID already exists"
            )

    employees.append(employee.dict())
    return {
        "message": "Employee added successfully",
        "employee": employee
    }


# Search employees by department
@app.get("/search")
def search_employee(department: str = Query(...)):
    result = [
        employee
        for employee in employees
        if employee["department"].lower() == department.lower()
    ]

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No employees found in this department"
        )

    return result


# Custom response
@app.get("/application-info")
def application_info():
    return JSONResponse(
        status_code=200,
        content={
            "application": "Employee Information API",
            "version": "1.0.0",
            "developer": "Your Name",
            "status": "Running"
        },
        headers={"X-Application": "EmployeeAPI"}
    )
