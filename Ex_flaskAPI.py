from flask import Flask, jsonify

app = Flask(__name__)

# List to store employee dictionaries
employees = [
    {"name": "Alice", "sal": 50000},
    {"name": "Bob", "sal": 60000}
]

@app.route("/employee/<name>")
def employee_by_name(name):
    return f"Employee name: {name}"

@app.route("/emps", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)