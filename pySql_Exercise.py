from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="employee_db"
)

cursor = db.cursor(dictionary=True)


# Home Route
@app.get("/")
def home():
    return jsonify({
        "application_name": "Employee Information API"
    })

# Get All Employees
@app.get("/employees")
def get_employees():

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    return jsonify(employees)

# Get One Employee
@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee:
        return jsonify(employee)

    return jsonify({"message": "Employee not found"}), 404


# Add Employee

@app.post("/employees")
def add_employee():

    data = request.json

    name = data["name"]
    department = data["department"]
    salary = data["salary"]

    sql = """
    INSERT INTO employees(name, department, salary)
    VALUES(%s,%s,%s)
    """

    cursor.execute(sql, (name, department, salary))
    db.commit()

    return jsonify({
        "message": "Employee Added Successfully"
    }), 201


# Search by Department

@app.get("/search")
def search_employee():

    department = request.args.get("department")

    cursor.execute(
        "SELECT * FROM employees WHERE department=%s",
        (department,)
    )

    employees = cursor.fetchall()

    return jsonify(employees)

# Custom Response Code

@app.get("/application-info")
def application_info():

    return jsonify({
        "application": "Employee Information API",
        "developer": "Jane",
        "version": "1.0"
    }), 202


# Run App

if __name__ == "__main__":
    app.run(debug=True)