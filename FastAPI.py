from fastapi import FastAPI, HTTPException

# Create the FastAPI app
app = FastAPI()

# Temporary list of employees (acts as our simple database)
employees = [
    {
        "id": 1,
        "name": "Alice Smith",
        "department": "Engineering",
        "role": "Developer",
    },
    {
        "id": 2,
        "name": "Bob Jones",
        "department": "HR",
        "role": "HR Manager",
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "department": "Engineering",
        "role": "Tester",
    },
]


# 1. GET / : Display application name
@app.get("/")
def home():
    return {"message": "Welcome to the Employee Information API!"}


# 2. GET /employees : Display all employees
@app.get("/employees")
def get_all_employees():
    return employees


# 3. GET /employees/{employee_id} : Display one employee by ID
@app.get("/employees/{employee_id}")
def get_one_employee(employee_id: int):
    for emp in employees:
        if emp["id"] == employee_id:
            return emp
    # If employee is not found, return a 404 error
    raise HTTPException(status_code=404, detail="Employee not found")


# 4. POST /employees : Add a new employee
@app.get("/search")
def search_employees_by_department(department: str):
    results = []
    for emp in employees:
        # Check if department matches (ignoring capital/small letters)
        if emp["department"].lower() == department.lower():
            results.append(emp)
    return results


# 5. GET /search : Search employees by department
@app.post("/employees")
def add_employee(new_emp: dict):
    # Give the new employee a simple automatic ID
    new_emp["id"] = len(employees) + 1
    employees.append(new_emp)
    return {"message": "Employee added successfully!", "employee": new_emp}


# 6. GET /application-info : Return custom response
@app.get("/application-info")
def get_application_info():
    return {
        "app_name": "Employee Info System",
        "version": "1.0.0",
        "status": "Running smoothly",
    }