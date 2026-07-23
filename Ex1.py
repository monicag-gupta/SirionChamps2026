from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="college"
)

cursor = db.cursor(dictionary=True)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return "Course CRUD API using Flask and MySQL"


# ---------------- GET ALL COURSES ----------------

@app.get("/courses")
def get_courses():

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return jsonify(courses)


# ---------------- ADD COURSE ----------------

@app.post("/courses/<name>/<duration>/<int:fee>")
def add_course(name, duration, fee):

    sql = "INSERT INTO courses(name, duration, fee) VALUES(%s,%s,%s)"
    values = (name, duration, fee)

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Course Added Successfully"})


# ---------------- SEARCH COURSE ----------------

@app.get("/courses/<int:id>")
def get_course(id):

    cursor.execute("SELECT * FROM courses WHERE id=%s", (id,))
    course = cursor.fetchone()

    if course:
        return jsonify(course)

    return jsonify({"message": "Course Not Found"})


# ---------------- UPDATE COURSE ----------------

@app.put("/courses/<int:id>/<name>/<duration>/<int:fee>")
def update_course(id, name, duration, fee):

    sql = """
    UPDATE courses
    SET name=%s, duration=%s, fee=%s
    WHERE id=%s
    """

    values = (name, duration, fee, id)

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Course Updated Successfully"})


# ---------------- DELETE COURSE ----------------

@app.delete("/courses/<int:id>")
def delete_course(id):

    cursor.execute("DELETE FROM courses WHERE id=%s", (id,))
    db.commit()

    return jsonify({"message": "Course Deleted Successfully"})


if __name__ == "__main__":
    app.run(debug=True)