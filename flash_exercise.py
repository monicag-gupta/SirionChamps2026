from flask import Flask, jsonify

app = Flask(__name__)

# List of employee dictionaries
employees = []

# GET /emps -> Returns all employees
@app.route("/emps", methods=["GET"])
def get_employees():
    return jsonify(employees)

# POST /emps/<name>/<int:sal> -> Adds a new employee
@app.route("/emps/<name>/<int:sal>", methods=["POST"])
def add_employee(name, sal):
    employee = {
        "name": name,
        "salary": sal
    }
    employees.append(employee)
    return jsonify({
        "message": "Employee added",
        "employee": employee
    }), 201

if __name__ == "__main__":
    app.run(debug=True)