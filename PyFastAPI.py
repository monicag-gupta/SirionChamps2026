from fastapi import FastAPI, HTTPException

app = FastAPI()

employees = [
    {"id": 1, "name": "Alice", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Bob", "department": "IT", "salary": 70000},
    {"id": 3, "name": "Charlie", "department": "Finance", "salary": 65000},
]


@app.get("/")
def home():
    return {"message": "Employee Information API"}


@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees")
def add_employee(employee: dict):
    employees.append(employee)
    return {"message": "Employee added", "employee": employee}


@app.get("/search")
def search(department: str):
    result = []
    for emp in employees:
        if emp["department"].lower() == department.lower():
            result.append(emp)
    return result


@app.get("/application-info")
def app_info():
    return {
        "application": "Employee Information API",
        "version": "1.0",
        "status": "Running"
    }
