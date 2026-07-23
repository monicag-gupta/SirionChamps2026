from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Employee Information API",
    description="A FastAPI application for managing employee records",
    version="1.0.0"
)


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=100)
    salary: float = Field(ge=0)
    location: Optional[str] = None


class EmployeeResponse(EmployeeCreate):
    employee_id: int


employees: list[EmployeeResponse] = [
    EmployeeResponse(
        employee_id=1,
        name="John Doe",
        department="Engineering",
        salary=50000,
        location="Bangalore"
    ),
    EmployeeResponse(
        employee_id=2,
        name="Jane Smith",
        department="Finance",
        salary=60000,
        location="Mumbai"
    ),
]


@app.get("/")
async def home():
    return {"application_name": "Employee Information API"}


@app.get("/employees", response_model=list[EmployeeResponse])
async def get_employees():
    return employees


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: Annotated[int, Path(ge=1)]):
    for employee in employees:
        if employee.employee_id == employee_id:
            return employee
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No employee with id {employee_id}"
    )


@app.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate):
    new_employee_id = (
        max(existing.employee_id for existing in employees) + 1
        if employees
        else 1
    )
    new_employee = EmployeeResponse(employee_id=new_employee_id, **employee.model_dump())
    employees.append(new_employee)
    return new_employee


@app.get("/search", response_model=list[EmployeeResponse])
async def search_employees(
    department: Annotated[
        Optional[str],
        Query(min_length=2, max_length=100)
    ] = None
):
    results = employees
    if department:
        results = [
            employee
            for employee in results
            if department.lower() in employee.department.lower()
        ]
    return results


@app.get("/application-info")
async def application_info():
    return {
        "name": "Employee Information API",
        "description": "A FastAPI app for managing employee records",
        "status": "running"
    }
