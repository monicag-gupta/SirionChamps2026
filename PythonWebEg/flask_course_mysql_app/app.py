from flask import Flask, jsonify, request

from database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"application_name": "Course Management API (MySQL-backed)"})


@app.get("/courses")
def get_courses():
    category = request.args.get("category")
    limit = request.args.get("limit", default=10, type=int)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if category:
        cursor.execute(
            "SELECT * FROM courses WHERE category LIKE %s LIMIT %s",
            (f"%{category}%", limit),
        )
    else:
        cursor.execute("SELECT * FROM courses LIMIT %s", (limit,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.get("/courses/<int:course_id>")
def get_course(course_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"error": f"No course with id {course_id}"}), 404
    return jsonify(row)


@app.post("/courses")
def create_course():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO courses (course_name, category, duration_hours, trainer, fee)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data.get("course_name"),
            data.get("category"),
            data.get("duration_hours"),
            data.get("trainer"),
            data.get("fee"),
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"course_id": new_id, **data}), 201


@app.put("/courses/<int:course_id>")
def update_course(course_id):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return jsonify({"error": f"No course with id {course_id}"}), 404

    cursor.execute(
        """
        UPDATE courses
        SET course_name = %s, category = %s, duration_hours = %s, trainer = %s, fee = %s
        WHERE course_id = %s
        """,
        (
            data.get("course_name"),
            data.get("category"),
            data.get("duration_hours"),
            data.get("trainer"),
            data.get("fee"),
            course_id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"course_id": course_id, **data})


@app.delete("/courses/<int:course_id>")
def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return jsonify({"error": f"No course with id {course_id}"}), 404

    cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Course {course_id} deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5002)
