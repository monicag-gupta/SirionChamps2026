from flask import Flask, jsonify

app = Flask(__name__)

# In-memory storage
employees = []


# Add employee
@app.route('/employee/<string:name>/<int:salary>', methods=['POST'])
def add_employee(name, salary):
    employee = {
        "name": name,
        "salary": salary
    }
    employees.append(employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": employee
    }), 201


# Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees), 200


if __name__ == '__main__':
    app.run(debug=True)
