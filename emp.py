from flask import Flask, request, jsonify

app = Flask(__name__)

employees = []

@app.route('/employees', methods=['POST'])
def add_employee():
    employee = {
        "name": request.args.get("name"),
        "id": request.args.get("id"),
        "salary": request.args.get("salary")
    }

    employees.append(employee)

    return jsonify(employee)

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
