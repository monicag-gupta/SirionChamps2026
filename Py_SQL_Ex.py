from flask import Flask, request
from database import get_connection

app = Flask(__name__)

@app.get("/")
def home():
    return "Employee API"

@app.get("/emps")
def get_all_employees():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees

@app.get("/emps/<int:emp_id>")
def get_employee(emp_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    if employee:
        return employee

    return {"message": "Employee not found"}, 404

@app.post("/emps")
def add_employee():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO employees(name, sal)
    VALUES(%s,%s)
    """

    values = (
        request.form["name"],
        request.form["sal"]
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Employee added successfully"}

@app.get("/search")
def search():
    name = request.args.get("name")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM employees WHERE name LIKE %s",
        ("%" + name + "%",)
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

@app.put("/emps/<int:emp_id>")
def update_employee(emp_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE employees
    SET name=%s, sal=%s
    WHERE id=%s
    """

    values = (
        request.form["name"],
        request.form["sal"],
        emp_id
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Employee updated successfully"}

@app.delete("/emps/<int:emp_id>")
def delete_employee(emp_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (emp_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Employee deleted successfully"}

@app.get("/application-info")
def application_info():
    return {
        "application": "Employee API",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(debug=True)
