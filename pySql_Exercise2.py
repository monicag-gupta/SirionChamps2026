from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="course_db"
)

cursor = db.cursor(dictionary=True)

# Home
@app.get("/")
def home():
    return jsonify({"message": "Course API with MySQL"})

# Insert
@app.post("/courses")
def add_course():
    data = request.get_json()

    sql = "INSERT INTO courses(name, duration, fee) VALUES(%s,%s,%s)"
    values = (
        data["name"],
        data["duration"],
        data["fee"]
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Course added successfully"})

# Get all courses
@app.get("/courses")
def get_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return jsonify(courses)

# Get course by id
@app.get("/courses/<int:id>")
def get_course(id):
    cursor.execute("SELECT * FROM courses WHERE id=%s", (id,))
    course = cursor.fetchone()

    if course:
        return jsonify(course)

    return jsonify({"message":"Course not found"})

# Update course
@app.put("/courses/<int:id>")
def update_course(id):
    data = request.get_json()

    sql = """
    UPDATE courses
    SET name=%s, duration=%s, fee=%s
    WHERE id=%s
    """

    values = (
        data["name"],
        data["duration"],
        data["fee"],
        id
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message":"Course updated"})

# Delete course
@app.delete("/courses/<int:id>")
def delete_course(id):
    cursor.execute("DELETE FROM courses WHERE id=%s", (id,))
    db.commit()

    return jsonify({"message":"Course deleted"})

if __name__ == "__main__":
    app.run(debug=True)