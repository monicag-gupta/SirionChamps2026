from flask import Flask, jsonify, request

app = Flask(__name__)

# List to store employee dictionaries
employees = [
    {"name": "Alice", "sal": 50000},
    {"name": "Bob", "sal": 60000}
]

@app.route("/employee/<name>")
def employee_by_name(name):
    return f"Employee name: {name}"

@app.route("/employee", methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route("/emps/<name>/<int:sal>", methods=["POST"])
def add_employee(name, sal):
    new_employee = {"name": name, "sal": sal}
    employees.append(new_employee)
    return jsonify({
        "message": "Employee added successfully!",
        "employee": new_employee
    }), 201

@app.route("/emps", methods=["GET"])
def get_employees():
    # Get the 'name' query parameter from URL (e.g. ?name=Alice)
    search_name = request.args.get("name")

    if search_name:
        # Filter employees whose name matches (case-insensitive)
        filtered = [
            emp for emp in employees 
            if emp["name"].lower() == search_name.lower()
        ]
        return jsonify(filtered)

    # If no 'name' parameter is provided, return all employees
    return jsonify(employees)

if __name__ == "__main__":
    app.run(debug=True)
