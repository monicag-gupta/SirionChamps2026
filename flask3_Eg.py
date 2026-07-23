from flask import Flask, request, jsonify

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

# 1. Home Route
@app.route("/", methods=["GET"])
def home():
    return "Employee Information API"

# 2. Display all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

# 3. Display one employee by ID
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)

    if employee:
        return jsonify(employee)

    return jsonify({"message": "Employee not found"}), 404

# 4. Add a new employee
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    new_employee = {
        "id": len(employees) + 1,
        "name": data.get("name"),
        "department": data.get("department"),
        "designation": data.get("designation")
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201

# 5. Search employees by department
@app.route("/search", methods=["GET"])
def search_employee():
    department = request.args.get("department")

    if not department:
        return jsonify({"message": "Please provide department"}), 400

    result = [
        emp for emp in employees
        if emp["department"].lower() == department.lower()
    ]

    return jsonify(result)

# 6. Application Information
@app.route("/application-info", methods=["GET"])
def application_info():
    return jsonify({
        "application": "Employee Information API",
        "version": "1.0",
        "developer": "Your Name"
    })

if __name__ == "__main__":
    app.run(debug=True)
