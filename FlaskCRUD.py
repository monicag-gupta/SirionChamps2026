from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


# Function to connect to MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="root@123",  # Change to your MySQL password
        database="simple_course_db",
    )


# 1. READ ALL COURSES (GET)
@app.route("/courses", methods=["GET"])
def get_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)  # dictionary=True gives us clean Python dicts

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(courses), 200


# 2. READ ONE COURSE (GET)
@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    course = cursor.fetchone()

    cursor.close()
    db.close()

    if course is None:
        return jsonify({"error": "Course not found!"}), 404

    return jsonify(course), 200


# 3. CREATE A NEW COURSE (POST)
@app.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json()

    title = data.get("title")
    instructor = data.get("instructor")

    db = get_db()
    cursor = db.cursor()

    # Insert into MySQL table
    sql = "INSERT INTO courses (title, instructor) VALUES (%s, %s)"
    cursor.execute(sql, (title, instructor))
    db.commit()  # Save changes to the database

    new_id = cursor.lastrowid  # Get the ID created by MySQL

    cursor.close()
    db.close()

    return (
        jsonify({"id": new_id, "title": title, "instructor": instructor}),
        201,
    )


# 4. UPDATE A COURSE (PUT)
@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.get_json()

    title = data.get("title")
    instructor = data.get("instructor")

    db = get_db()
    cursor = db.cursor()

    # Update database
    sql = "UPDATE courses SET title = %s, instructor = %s WHERE id = %s"
    cursor.execute(sql, (title, instructor, course_id))
    db.commit()

    cursor.close()
    db.close()

    return (
        jsonify(
            {"id": course_id, "title": title, "instructor": instructor}
        ),
        200,
    )


# 5. DELETE A COURSE (DELETE)
@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    db = get_db()
    cursor = db.cursor()

    sql = "DELETE FROM courses WHERE id = %s"
    cursor.execute(sql, (course_id,))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Course deleted successfully!"}), 200


# Run app
if __name__ == "__main__":
    app.run(debug=True)