from flask import Flask, jsonify, request

app = Flask(__name__)

# Employee list
employees = [
    {"id": 1, "name": "John", "department": "IT", "sal": 50000},
    {"id": 2, "name": "Alice", "department": "HR", "sal": 60000}
]


# Home
@app.get("/")
def home():
    return jsonify({
        "application_name": "Employee API"
    })


# Get all employees
@app.get("/employees")
def get_employees():
    return jsonify(employees)


# Get employee by ID
@app.get("/employees/<int:id>")
def get_employee(id):
    for emp in employees:
        if emp["id"] == id:
            return jsonify(emp)

    return jsonify({"error": "Employee not found"}), 404


# Add employee
@app.post("/employees")
def add_employee():
    data = request.get_json()

    new_employee = {
        "id": max([emp["id"] for emp in employees], default=0) + 1,
        "name": data.get("name"),
        "department": data.get("department"),
        "sal": data.get("sal")
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201


# Search employee by department
@app.get("/search")
def search_employee():
    department = request.args.get("department")

    result = employees

    if department:
        result = [
            emp for emp in employees
            if department.lower() == emp["department"].lower()
        ]

    return jsonify(result)


# Application Info
@app.get("/application-info")
def application_info():
    return jsonify({
        "name": "Employee API",
        "description": "Flask API to manage employee records",
        "status": "Running"
    }), 202


if __name__ == "__main__":
    app.run(debug=True)