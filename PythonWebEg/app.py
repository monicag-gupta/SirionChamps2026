from flask import Flask, request, jsonify

from models import Employee

app = Flask(__name__)

employees_db = [
    Employee(1, "John Doe", 50000),
    Employee(2, "Jane Smith", 60000),
]

@app.route("/")
def home():
    return "Home Page"

@app.route("/about")
def about():
    return "About Us"

@app.route("/contact")
def contact():
    return "Contact Us"

@app.route("/employees")
def employees():
    return "Employee List"

@app.get("/emps")
def get_employees():
    return jsonify([e.to_dict() for e in employees_db])

@app.post("/emps")
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        id=data.get("id"),
        name=data.get("name"),
        salary=data.get("salary"),
    )
    employees_db.append(new_employee)
    return jsonify(new_employee.to_dict()), 201

@app.route("/employee", methods=["GET", "POST"])
def employee():
    return "Employee request received"

@app.post("/emps/<int:id>/<name>/<int:salary>")
def add_employee_path(id, name, salary):
    new_employee = Employee(id=id, name=name, salary=salary)
    employees_db.append(new_employee)
    return jsonify(new_employee.to_dict()), 201



if __name__ == "__main__":
    app.run(debug=True)