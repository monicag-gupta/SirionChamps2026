import pymysql.cursors
from flask import Flask, jsonify, request

from flaskext.mysql import MySQL

app = Flask(__name__)

# --- MySQL Configuration ---
mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "root@123"
app.config["MYSQL_DATABASE_DB"] = "EmpData"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)


# --- Database Helper Function ---
def get_db_cursor():
    """Establishes DB connection and returns conn and a DictCursor tuple."""
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor


# --- Routes ---


@app.route("/")
def home():
    return "Employee Information API"


@app.route("/employees", methods=["GET"])
def get_employees():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT id, name, role, department FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return jsonify(employees)


@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    conn, cursor = get_db_cursor()
    cursor.execute(
        "SELECT id, name, role, department FROM employees WHERE id = %s",
        (employee_id,),
    )
    employee = cursor.fetchone()
    conn.close()

    if employee:
        return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404


@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json() or {}
    name = data.get("name")
    role = data.get("role", "Staff")
    department = data.get("department")

    if not name or not department:
        return jsonify({"error": "Name and department are required fields"}), 400

    conn, cursor = get_db_cursor()
    query = "INSERT INTO employees (name, role, department) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, role, department))
    conn.commit()  # Save changes to database

    new_id = cursor.lastrowid
    conn.close()

    new_emp = {
        "id": new_id,
        "name": name,
        "role": role,
        "department": department,
    }
    return jsonify(new_emp), 201


@app.route("/search", methods=["GET"])
def search():
    dept = request.args.get("department", "")

    conn, cursor = get_db_cursor()
    cursor.execute(
        "SELECT id, name, role, department FROM employees WHERE LOWER(department) = LOWER(%s)",
        (dept,),
    )
    results = cursor.fetchall()
    conn.close()

    return jsonify(results)


@app.route("/application-info", methods=["GET"])
def app_info():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM employees")
    result = cursor.fetchone()
    conn.close()

    return jsonify(
        {
            "status": "Running",
            "version": "1.0",
            "total_employees": result["total"] if result else 0,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)