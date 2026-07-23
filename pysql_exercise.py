from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", "root@123"),
    database=os.getenv("MYSQL_DATABASE", "employee_db")
)

cursor = db.cursor(dictionary=True)

@app.get("/")
def home():
    return "Employee Information API"

# Get all employees
@app.get("/employees")
def get_all_employees():
    cursor.execute("SELECT * FROM employee")
    return cursor.fetchall()

# Get one employee
@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    cursor.execute("SELECT * FROM employee WHERE id=%s", (employee_id,))
    employee = cursor.fetchone()

    if employee:
        return employee

    return {"message": "Employee not found"}, 404

# Add employee
@app.post("/employees")
def add_employee():
    id = request.form["id"]
    name = request.form["name"]
    department = request.form["department"]
    salary = request.form["salary"]

    sql = """
    INSERT INTO employee(id, name, department, salary)
    VALUES(%s, %s, %s, %s)
    """

    cursor.execute(sql, (id, name, department, salary))
    db.commit()

    return {"message": "Employee added successfully"}

# Search by department
@app.get("/search")
def search():
    department = request.args.get("department")

    cursor.execute(
        "SELECT * FROM employee WHERE department=%s",
        (department,)
    )

    return cursor.fetchall()

# Application info
@app.get("/application-info")
def application_info():
    return {
        "application": "Employee Information API",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(debug=True)
