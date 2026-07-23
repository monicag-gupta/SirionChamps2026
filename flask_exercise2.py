from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Sample employee data
employees = [
    {
        "id": 1,
        "name": "Alice",
        "department": "HR",
        "designation": "Manager"
    },
    {
        "id": 2,
        "name": "Bob",
        "department": "IT",
        "designation": "Developer"
    },
    {
        "id": 3,
        "name": "Charlie",
        "department": "Finance",
        "designation": "Accountant"
    }
]

# Route 1: Display application name
@app.route("/", methods=["GET"])
def home():
    return "Employee Information API"


# Route 2: Display all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)


# Route 3: Display one employee by ID
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return jsonify(employee)
    return jsonify({"message": "Employee not found"}), 404


# Route 4: Add a new employee
@app.route("/employees", methods=["POST"])
def add_employee():
    new_employee = request.get_json()

    if not new_employee:
        return jsonify({"message": "Invalid data"}), 400

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201


# Route 5: Search employees by department
@app.route("/search", methods=["GET"])
def search_employee():
    department = request.args.get("department")

    if not department:
        return jsonify({"message": "Please provide department"}), 400

    result = [
        employee for employee in employees
        if employee["department"].lower() == department.lower()
    ]

    return jsonify(result)


# Route 6: Return a custom response
@app.route("/application-info", methods=["GET"])
def application_info():
    response = make_response(
        jsonify({
            "application": "Employee Information API",
            "version": "1.0",
            "developer": "Your Name"
        }),
        200
    )
    response.headers["Custom-Header"] = "EmployeeAPI"
    return response


if __name__ == "__main__":
    app.run(debug=True)