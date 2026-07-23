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

# The path converter accepts text containing forward slashes.
@app.route("/department/<path:department_name>")
def department(department_name):
    return f"Department: {department_name}"



@app.route("/empl/<int:employee_id>")
def employee_by_id(employee_id):
    return f"Employee ID: {employee_id}"

@app.route("/salary/<float:amount>")
def salary(amount):
    return f"Employee salary: {amount}"

@app.post("/emps/<int:id>/<name>/<int:salary>")
def add_employee_path(id, name, salary):
    new_employee = Employee(id=id, name=name, salary=salary)
    employees_db.append(new_employee)
    return jsonify(new_employee.to_dict()), 201

@app.get("/emps/search")
def search_employees():
    name = request.args.get("name")
    id_param = request.args.get("id")
    salary_param = request.args.get("salary")

    results = employees_db
    if name:
        results = [e for e in results if name.lower() in e.name.lower()]
    if id_param:
        results = [e for e in results if e.id == int(id_param)]
    if salary_param:
        results = [e for e in results if e.salary == float(salary_param)]

    return jsonify([e.to_dict() for e in results])



if __name__ == "__main__":
    app.run(debug=True)