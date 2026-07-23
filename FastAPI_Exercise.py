from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Employee Information API")

employees = [
    {
        "id": 1,
        "name": "John",
        "department": "HR",
        "salary": 50000
    },
    {
        "id": 2,
        "name": "Alice",
        "department": "IT",
        "salary": 70000
    },
    {
        "id": 3,
        "name": "Bob",
        "department": "Finance",
        "salary": 65000
    }
]



@app.get("/")
def home():
    return {"Application": "Employee Information API"}

@app.get("/employees")
def get_employees():
    return employees

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for emp in employees:
        if emp["id"] == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees")
def add_employee(employee: dict):
    employees.append(employee)
    return {
        "message": "Employee added successfully",
        "employee": employee
    }

@app.get("/search")
def search_employee(department: str):
    result = [
        emp for emp in employees
        if emp["department"].lower() == department.lower()
    ]

    if not result:
        return {"message": "No employee found"}

    return result


@app.get("/application-info")
def application_info():
    return JSONResponse(
        status_code=200,
        content={
            "application": "Employee Information API",
            "version": "1.0",
            "developer": "Jane",
            "status": "Running Successfully"
        }
    )