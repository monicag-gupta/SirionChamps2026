from flask import Flask, jsonify, request, abort

app = Flask(__name__)

EMPLOYEES = [
    {"id": 1, "name": "Alice", "role": "Developer", "department": "Engineering"},
    {"id": 2, "name": "Bob", "role": "Designer", "department": "UX"},
    {"id": 3, "name": "Alice", "role": "Manager", "department": "HR"},
]

@app.route("/")
def home():
    return "Employee Information API"

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(EMPLOYEES)

@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    for emp in EMPLOYEES:
        if emp["id"] == employee_id:
            return jsonify(emp)
    return jsonify({"error": "Employee not found"}), 404

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    new_emp = {
        "id": len(EMPLOYEES) + 1,
        "name": data.get("name"),
        "role": data.get("role", "Staff"),
        "department": data.get("department")
    }
    EMPLOYEES.append(new_emp)
    return jsonify(new_emp), 201

@app.route("/search", methods=["GET"])
def search():
    dept = request.args.get("department", "")
    result = [emp for emp in EMPLOYEES if emp["department"].lower() == dept.lower()]
    return jsonify(result)

@app.route("/application-info", methods=["GET"])
def app_info():
    return jsonify({
        "status": "Running",
        "version": "1.0",
        "total_employees": len(EMPLOYEES)
    })

if __name__ == "__main__":
    app.run(debug=True)