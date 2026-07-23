from fastapi import FastAPI

app = FastAPI()

employees = [
    {"id": 1, "name": "John", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Alice", "department": "IT", "salary": 70000},
    {"id": 3, "name": "Bob", "department": "Finance", "salary": 60000}
]

# Display application name
@app.get("/")
def home():
    return {"message": "Employee Information API"}

# Display all employees
@app.get("/employees")
def get_all_employees():
    return employees

# Display one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    return {"message": "Employee not found"}

# Add a new employee
@app.post("/employees")
def add_employee(id: int, name: str, department: str, salary: int):
    employee = {
        "id": id,
        "name": name,
        "department": department,
        "salary": salary
    }

    employees.append(employee)
    return {"message": "Employee added successfully"}

# Search employees by department
@app.get("/search")
def search(department: str):
    result = []

    for employee in employees:
        if employee["department"].lower() == department.lower():
            result.append(employee)

    return result

# Application information
@app.get("/application-info")
def application_info():
    return {
        "application": "Employee Information API",
        "version": "1.0",
        "framework": "FastAPI"
    }
