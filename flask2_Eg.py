from flask import Flask, jsonify, request

app = Flask(__name__)

# List of employee dictionaries
employees = [
    {"id": 1, "name": "Alice", "salary": 50000},
    {"id": 2, "name": "Bob", "salary": 60000},
    {"id": 3, "name": "Charlie", "salary": 70000}
]


# Home route
@app.route("/")
def home():
    return "Employee Management API"


# Get all employees
@app.route("/employees", methods=["GET"])
def get_all_employees():
    return jsonify(employees)


# Search employee by name using query parameter
@app.route("/employees/search", methods=["GET"])
def search_employee():
    name = request.args.get("name")

    if not name:
        return jsonify({"message": "Please provide employee name"}), 400

    result = []

    for emp in employees:
        if emp["name"].lower() == name.lower():
            result.append(emp)

    if result:
        return jsonify(result)

    return jsonify({"message": "Employee not found"}), 404


# Get employee by ID using path parameter
@app.route("/employee/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    for emp in employees:
        if emp["id"] == emp_id:
            return jsonify(emp)

    return jsonify({"message": "Employee not found"}), 404


# Create new employee
@app.route("/employee", methods=["POST"])
def create_employee():

    data = request.get_json()

    new_employee = {
        "id": len(employees) + 1,
        "name": data["name"],
        "salary": data["salary"]
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee created successfully",
        "employee": new_employee
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
