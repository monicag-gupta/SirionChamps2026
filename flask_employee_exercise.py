from flask import Flask

app = Flask(__name__)

employees = [{"name": "John", "salary": 60000}]

@app.post('/employee/<string:name>/<int:salary>')
def add_employee(name, salary):
    employees.append({
        "name": name,
        "salary": salary
    })
    return "Employee added successfully"

@app.get('/employees')
def get_employees():
    return str(employees)

if __name__ == "__main__":
    app.run(debug=True)
