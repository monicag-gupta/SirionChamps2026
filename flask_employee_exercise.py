from flask import Flask, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "John", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Alice", "department": "IT", "salary": 70000},
    {"id": 3, "name": "Bob", "department": "Finance", "salary": 60000}
]

@app.get("/")
def home():
    return "Employee Information API"

@app.get("/employees")
def get_all_employees():
    return employees

@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    return {"message": "Employee not found"}, 404

@app.post("/employees")
def add_employee():
    employee = {
        "id": int(request.form["id"]),
        "name": request.form["name"],
        "department": request.form["department"],
        "salary": int(request.form["salary"])
    }

    employees.append(employee)
    return {"message": "Employee added successfully"}

@app.get("/search")
def search():
    department = request.args.get("department")

    result = []
    for employee in employees:
        if employee["department"].lower() == department.lower():
            result.append(employee)

    return result

@app.get("/application-info")
def application_info():
    return {
        "application": "Employee Information API",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(debug=True)
