from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

# Initialize the application
app = FastAPI(title="Employee Information API")

# Pydantic model for data validation
class Employee(BaseModel):
    id: int
    name: str
    department: str
    role: str

# In-memory database
employees_db = [
    {"id": 1, "name": "Alice Smith", "department": "Engineering", "role": "Backend Developer"},
    {"id": 2, "name": "Bob Jones", "department": "HR", "role": "HR Manager"},
    {"id": 3, "name": "Charlie Davis", "department": "Engineering", "role": "Frontend Developer"},
]

# 1. GET / - Display the application name
@app.get("/")
def read_root():
    return {"application_name": "Employee Information API"}

# 2. GET /employees - Display all employees
@app.get("/employees", response_model=List[Employee])
def get_all_employees():
    return employees_db

# 3. GET /employees/{employee_id} - Display one employee
@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    for emp in employees_db:
        if emp["id"] == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

# 4. POST /employees - Add a new employee
@app.post("/employees", response_model=Employee, status_code=201)
def add_employee(employee: Employee):
    # Check if ID already exists
    if any(emp["id"] == employee.id for emp in employees_db):
        raise HTTPException(status_code=400, detail="Employee with this ID already exists")
    
    employees_db.append(employee.dict())
    return employee

# 5. GET /search - Search employees by department
@app.get("/search", response_model=List[Employee])
def search_employees(department: str = Query(..., description="The department to search for")):
    results = [emp for emp in employees_db if emp["department"].lower() == department.lower()]
    if not results:
        raise HTTPException(status_code=404, detail=f"No employees found in the {department} department")
    return results

# 6. GET /application-info - Return a custom response
@app.get("/application-info")
def get_app_info():
    content = {
        "status": "Healthy",
        "version": "1.0.0",
        "description": "API for managing internal employee records.",
        "author": "Internal IT"
    }
    # Using JSONResponse allows you to customize headers and status codes easily
    return JSONResponse(content=content, status_code=200, headers={"X-Custom-Header": "Emp-API"})