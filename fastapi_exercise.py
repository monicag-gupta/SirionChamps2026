from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Employee Information API")


# Employee Model
class Employee(BaseModel):
    id: int
    name: str
    department: str
    designation: str


# Sample Data
employees = [
    {"id": 1, "name": "Alice", "department": "HR", "designation": "Manager"},
    {"id": 2, "name": "Bob", "department": "IT", "designation": "Developer"},
    {"id": 3, "name": "Charlie", "department": "Finance", "designation": "Accountant"},
]


# Route 1: Display application name
@app.get("/")
def home():
    return {"message": "Employee Information API"}


# Route 2: Display all employees
@app.get("/employees")
def get_employees():
    return employees


# Route 3: Display one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


# Route 4: Add a new employee
@app.post("/employees")
def add_employee(employee: Employee):
    employees.append(employee.dict())
    return {
        "message": "Employee added successfully",
        "employee": employee
    }


# Route 5: Search employees by department
@app.get("/search")
def search_employees(department: str = Query(...)):
    result = [
        emp for emp in employees
        if emp["department"].lower() == department.lower()
    ]
    return result


# Route 6: Return a custom response
@app.get("/application-info")
def application_info():
    return JSONResponse(
        content={
            "application": "Employee Information API",
            "version": "1.0",
            "developer": "Your Name"
        },
        headers={"Custom-Header": "EmployeeAPI"}
    )