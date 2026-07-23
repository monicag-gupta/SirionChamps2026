from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Change if needed
    password="root",  # Change to your MySQL password
    database="employee_db"
)

cursor = db.cursor(dictionary=True)

# 1. Home Route
@app.route("/", methods=["GET"])
def home():
    return "Employee Information API"

# 2. Display all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return jsonify(employees)

# 3. Display one employee
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    cursor.execute("SELECT * FROM employees WHERE id=%s", (employee_id,))
    employee = cursor.fetchone()

    if employee:
        return jsonify(employee)

    return jsonify({"message": "Employee not found"}), 404

# 4. Add a new employee
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()

    query = """
        INSERT INTO employees (name, department, designation)
        VALUES (%s, %s, %s)
    """

    values = (
        data["name"],
        data["department"],
        data["designation"]
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({
        "message": "Employee added successfully",
        "employee_id": cursor.lastrowid
    }), 201

# 5. Search employees by department
@app.route("/search", methods=["GET"])
def search_department():
    department = request.args.get("department")

    cursor.execute(
        "SELECT * FROM employees WHERE department=%s",
        (department,)
    )

    employees = cursor.fetchall()

    return jsonify(employees)

# 6. Application Information
@app.route("/application-info", methods=["GET"])
def application_info():
    return jsonify({
        "application": "Employee Information API",
        "database": "MySQL",
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run(debug=True)
