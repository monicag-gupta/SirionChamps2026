from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

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
    return "Employee API"

@app.get("/emps")
def get_all_employees():
    cursor.execute("SELECT * FROM employee")
    return cursor.fetchall()

@app.get("/emps/<int:emp_id>")
def get_employee(emp_id):
    cursor.execute("SELECT * FROM employee WHERE id=%s", (emp_id,))
    emp = cursor.fetchone()

    if emp:
        return emp

    return {"message": "Employee not found"}, 404

@app.post("/emps")
def add_employee():
    id = request.form["id"]
    name = request.form["name"]
    sal = request.form["sal"]

    sql = """
    INSERT INTO employee(id, name, sal)
    VALUES(%s, %s, %s)
    """

    cursor.execute(sql, (id, name, sal))
    db.commit()

    return {"message": "Employee added successfully"}

@app.get("/search")
def search():
    name = request.args.get("name")

    cursor.execute(
        "SELECT * FROM employee WHERE name=%s",
        (name,)
    )

    return cursor.fetchall()

@app.put("/emps/<int:emp_id>")
def update_employee(emp_id):
    name = request.form["name"]
    sal = request.form["sal"]

    sql = """
    UPDATE employee
    SET name=%s, sal=%s
    WHERE id=%s
    """

    cursor.execute(sql, (name, sal, emp_id))
    db.commit()

    return {"message": "Employee updated successfully"}

@app.delete("/emps/<int:emp_id>")
def delete_employee(emp_id):
    cursor.execute(
        "DELETE FROM employee WHERE id=%s",
        (emp_id,)
    )

    db.commit()

    return {"message": "Employee deleted successfully"}

@app.get("/application-info")
def application_info():
    return {
        "application": "Employee API",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(debug=True)    return {"message": "Employee not found"}, 404

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
