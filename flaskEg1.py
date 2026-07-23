from flask import Flask, jsonify

app = Flask(__name__)

# Employee list
employees = [
    {
        "id": 1,
        "name": "John",
        "salary": 50000
    }
]


# Get all employees
@app.get("/employees")
def get_employees():
    return jsonify(employees)


# Add employee using path parameters
@app.post("/employees/<name>/<int:salary>")
def add_employee(name, salary):

    employee = {
        "id": len(employees) + 1,
        "name": name,
        "salary": salary
    }

    employees.append(employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": employee
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
