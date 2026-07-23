from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Employee Management API",
    description="FastAPI introduction and validation example",
    version="1.0.0"
)

class EmpCreate(BaseModel):
    emp_name: str = Field(
        min_length=2,
        max_length=150
    )

class EmpResponse(EmpCreate):
    emp_id: int

employees: list[EmpResponse] = [
    EmpResponse(
        emp_id=101,
        emp_name="John",
    ),
    EmpResponse(
        emp_id=102,
        emp_name="Jennie",
    ),
    EmpResponse(
       emp_id=103,
       emp_name="Bob",
    )
]

@app.get("/")
async def home():
    return {
        "application": "Employee Management API",
        "framework": "FastAPI",
        "status": "running"
    }

@app.get(
    "/employees",
    response_model=list[EmpResponse]
)
async def get_all_employees(
    category: Annotated[
        Optional[str],
        Query(min_length=2, max_length=100)
    ] = None,
    limit: Annotated[
        int,
        Query(ge=1, le=100)
    ] = 10
):
    results = employees
    if category:
        results = [
            employee
            for employee in results
            if category.lower()
            in employee.emp_name.lower()
        ]
    return results[:limit]

@app.get(
    "/employees/{emp_id}",
    response_model=EmpResponse
)
async def get_course(
    emp_id: Annotated[
        int,
        Path(ge=1)
    ]
):
    for employee in employees:
        if employee.emp_id == emp_id:
            return employee
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

@app.post(
    "/employees",
    response_model=EmpResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee: EmpCreate
):
    new_emp_id = (
        max(
            existing_employee.emp_id
            for existing_employee in employees
        )
        + 1
        if employees
        else 101
    )
    new_employee = EmpResponse(
        emp_id=new_emp_id,
        **employee.model_dump()
    )
    employees.append(new_employee)
    return new_employee

@app.get("/search", response_model=list[EmpResponse])
async def search_employees(
    name: Annotated[str, Query(min_length=1, description="Name keyword to search")]
):
    return [
        emp for emp in employees 
        if name.lower() in emp.emp_name.lower()
    ]

@app.get("/application-info")
async def get_application_info():
    return {
        "application": "Employee Management API",
        "framework": "FastAPI",
        "version": "1.0.0",
        "status": "running"
    }