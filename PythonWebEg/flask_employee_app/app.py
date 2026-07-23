from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {"employee_id": 1, "name": "John Doe", "department": "Engineering", "salary": 50000, "location": "Bangalore"},
    {"employee_id": 2, "name": "Jane Smith", "department": "Finance", "salary": 60000, "location": "Mumbai"},
]


def next_id():
    return max((e["employee_id"] for e in employees), default=0) + 1


@app.get("/")
def home():
    return jsonify({"application_name": "Employee Information API"})


@app.get("/employees")
def get_employees():
    return jsonify(employees)


@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    for employee in employees:
        if employee["employee_id"] == employee_id:
            return jsonify(employee)
    return jsonify({"error": f"No employee with id {employee_id}"}), 404


@app.post("/employees")
def add_employee():
    data = request.get_json()
    new_employee = {
        "employee_id": next_id(),
        "name": data.get("name"),
        "department": data.get("department"),
        "salary": data.get("salary"),
        "location": data.get("location"),
    }
    employees.append(new_employee)
    return jsonify(new_employee), 201


@app.get("/search")
def search_employees():
    department = request.args.get("department")
    results = employees
    if department:
        results = [e for e in results if department.lower() in (e.get("department") or "").lower()]
    return jsonify(results)


@app.get("/application-info")
def application_info():
    return jsonify({
        "name": "Employee Information API",
        "description": "A Flask API for managing employee records",
        "status": "running",
    })


if __name__ == "__main__":
    app.run(debug=True, port=5003)
