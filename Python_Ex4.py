from flask import Flask, jsonify

app = Flask(__name__)

# List of employee dictionaries
emps = [
    {"name": "Rohit", "sal": 50000},
    {"name": "Aman", "sal": 60000},
    {"name": "Priya", "sal": 55000}
]

# GET API - Returns all employees
@app.route("/emps", methods=["GET"])
def get_emps():
    return jsonify(emps)

# POST API - Adds a new employee
@app.route("/emps/<name>/<int:sal>", methods=["POST"])
def add_emp(name, sal):
    emp = {
        "name": name,
        "sal": sal
    }
    emps.append(emp)

    return jsonify({
        "message": "Employee added successfully",
        "employee": emp,
        "employees": emps
    }), 201

@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")

    for emp in emps:
        if emp["name"].lower() == name.lower():
            return jsonify(emp)

    return jsonify({"message": "Employee not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
