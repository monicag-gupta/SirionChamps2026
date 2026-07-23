from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="company"
)

cursor = db.cursor(dictionary=True)

# Add Employee
@app.route("/employee/<name>/<int:emp_id>/<int:salary>", methods=["POST"])
def add_employee(name, emp_id, salary):
    query = "INSERT INTO employees (id, name, salary) VALUES (%s, %s, %s)"
    values = (emp_id, name, salary)

    try:
        cursor.execute(query, values)
        db.commit()
        return jsonify({
            "id": emp_id,
            "name": name,
            "salary": salary,
            "message": "Employee added successfully"
        })
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


# Get All Employees
@app.route("/employees", methods=["GET"])
def get_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return jsonify(employees)


# Search Employee by Name
@app.route("/search/<name>", methods=["GET"])
def search_employee(name):
    query = "SELECT * FROM employees WHERE LOWER(name)=LOWER(%s)"
    cursor.execute(query, (name,))
    employee = cursor.fetchone()

    if employee:
        return jsonify(employee)
    else:
        return jsonify({"message": "Employee not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)