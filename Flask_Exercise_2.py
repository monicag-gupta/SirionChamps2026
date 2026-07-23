from flask import Flask

app = Flask(__name__)

# List of employee dictionaries
employees = [
    {"name": "Rahul", "sal": 50000},
    {"name": "Priya", "sal": 60000}
]

# GET /emps -> Returns the employee list
@app.get("/emps")
def get_employees():
    return employees

# POST /emps/<name>/<sal> -> Adds a new employee
@app.post("/emps/<name>/<int:sal>")
def add_employee(name, sal):
    employee = {
        "name": name,
        "sal": sal
    }

    employees.append(employee)

    return {
        "message": "Employee added successfully",
        "employee": employee
    }

if __name__ == "__main__":
    app.run(debug=True)