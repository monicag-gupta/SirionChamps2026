from flask import Flask, request

app = Flask(__name__)

employees = [{"name": "John", "salary": 60000},
    {"name": "Alice", "salary": 75000},
    {"name": "Bob", "salary": 55000}]

@app.post('/employee/<string:name>/<int:salary>')
def add_employee(name, salary):
    employees.append({
        "name": name,
        "salary": salary
    })
    return "Employee added successfully"

@app.get('/employees')
def get_employees():
    return employees

@app.route("/search")
def search_employee():
    name = request.args.get("name")
    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee
    return "Employee not found"

if __name__ == "__main__":
    app.run(debug=True)
