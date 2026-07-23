from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Employee list
employees = [
    {
        "id": 1,
        "name": "Ayush",
        "age": 22,
        "department": "IT",
        "salary": 50000
    },
    {
        "id": 2,
        "name": "Rahul",
        "age": 25,
        "department": "HR",
        "salary": 45000
    },
    {
        "id": 3,
        "name": "Sneha",
        "age": 24,
        "department": "Finance",
        "salary": 60000
    }
]


# 1. Home Route
@app.get("/")
def home():
    return {"Application": "Employee Information API"}


# 2. Display all employees
@app.get("/employees")
def get_employees():
    return employees


# 3. Display one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return {"message": "Employee not found"}


# 4. Add a new employee
@app.post("/employees")
def add_employee(employee: dict):

    employees.append(employee)

    return {
        "message": "Employee added successfully",
        "employee": employee
    }


# 5. Search employees by department
# Example:
# http://127.0.0.1:8000/search?department=IT
@app.get("/search")
def search_employee(department: str):

    result = []

    for employee in employees:
        if employee["department"].lower() == department.lower():
            result.append(employee)

    return result


# 6. Custom Response
@app.get("/application-info")
def application_info():

    return JSONResponse(
        status_code=200,
        content={
            "Application": "Employee Information API",
            "Version": "1.0",
            "Developer": "Ayush",
            "Status": "Running Successfully"
        }
    )