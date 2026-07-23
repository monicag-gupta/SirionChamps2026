from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI(title="Employee Information API")

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",   # Change to your MySQL password
    database="employee_db"
)

cursor = db.cursor(dictionary=True)


# Pydantic Model
class Employee(BaseModel):
    name: str
    department: str
    designation: str


# 1. Home Route
@app.get("/")
def home():
    return {"message": "Employee Information API"}


# 2. Display all employees
@app.get("/employees")
def get_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return employees


# 3. Display one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee:
        return employee

    raise HTTPException(status_code=404, detail="Employee not found")


# 4. Add a new employee
@app.post("/employees")
def add_employee(employee: Employee):

    query = """
        INSERT INTO employees (name, department, designation)
        VALUES (%s, %s, %s)
    """

    values = (
        employee.name,
        employee.department,
        employee.designation
    )

    cursor.execute(query, values)
    db.commit()

    return {
        "message": "Employee added successfully",
        "employee_id": cursor.lastrowid
    }


# 5. Search employees by department
@app.get("/search")
def search_employee(department: str):

    cursor.execute(
        "SELECT * FROM employees WHERE department=%s",
        (department,)
    )

    employees = cursor.fetchall()

    return employees


# 6. Application Information
@app.get("/application-info")
def application_info():
    return {
        "application": "Employee Information API",
        "framework": "FastAPI",
        "database": "MySQL",
        "version": "1.0"
    }
