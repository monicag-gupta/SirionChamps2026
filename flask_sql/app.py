from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          # Replace with your MySQL username
    password="Devesh@2004",  # Replace with your MySQL password
    database="course_db"
)

cursor = db.cursor(dictionary=True)

# Home Route
@app.route('/')
def home():
    return "Course CRUD API using Flask and MySQL"

# Get All Courses
@app.route('/courses', methods=['GET'])
def get_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return jsonify(courses)

# Get Single Course
@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    cursor.execute("SELECT * FROM courses WHERE id=%s", (id,))
    course = cursor.fetchone()

    if course:
        return jsonify(course)
    else:
        return jsonify({"message": "Course not found"}), 404

# Add Course
@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()

    sql = """
    INSERT INTO courses(course_name, instructor, duration)
    VALUES(%s, %s, %s)
    """

    values = (
        data['course_name'],
        data['instructor'],
        data['duration']
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Course added successfully"}), 201

# Update Course
@app.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.get_json()

    sql = """
    UPDATE courses
    SET course_name=%s,
        instructor=%s,
        duration=%s
    WHERE id=%s
    """

    values = (
        data['course_name'],
        data['instructor'],
        data['duration'],
        id
    )

    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Course not found"}), 404

    return jsonify({"message": "Course updated successfully"})

# Delete Course
@app.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    cursor.execute("DELETE FROM courses WHERE id=%s", (id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Course not found"}), 404

    return jsonify({"message": "Course deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
