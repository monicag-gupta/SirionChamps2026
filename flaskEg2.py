from flask import Flask, jsonify,request

app = Flask(__name__)


EMPLOYEES = [
    {"id": 1, "name": "Alice", "role": "Developer", "department": "Engineering"},
    {"id": 2, "name": "Bob", "role": "Designer", "department": "UX"},
    {"id": 3, "name": "Alice", "role": "Manager", "department": "HR"},
]



@app.route("/")
def home():
    return "Home Page"

@app.route("/about")
def about():
    return "About Us"

@app.route("/contact")
def contact():
    return "Contact Us"

# --- EMPLOYEE ROUTES ---

# GET: Fetch all employees
@app.get("/emps")
def get_employees():
    return jsonify({"status": "success", "data": EMPLOYEES})


# GET: Find employees matching a name (Case-insensitive)
@app.get("/employee/<name>")
def employee_by_name(name):
    matching_employees = [
        emp for emp in EMPLOYEES 
        if emp["name"].lower() == name.lower()
    ]
    
    if not matching_employees:
        return jsonify({
            "status": "error", 
            "message": f"No employee found with name '{name}'"
        }), 404
        
    return jsonify({"status": "success", "data": matching_employees})


# POST: Add a new employee using URL parameters (/employee/<name>/<emp_id>)
@app.route("/employee/<name>/<int:emp_id>", methods=["GET", "POST"])
def add_employee_by_url(name, emp_id):
    # 1. Check if an employee with this ID already exists
    if any(emp["id"] == emp_id for emp in EMPLOYEES):
        return jsonify({
            "status": "error",
            "message": f"Employee with ID {emp_id} already exists."
        }), 400

    # 2. Build new employee object
    new_employee = {
        "id": emp_id,
        "name": name,
        "role": "General",
        "department": "Unassigned"
    }

    # 3. Add to our list
    EMPLOYEES.append(new_employee)

    # 4. Return success response (201 Created)
    return jsonify({
        "status": "success",
        "message": f"Employee '{name}' with ID {emp_id} created successfully.",
        "data": new_employee
    }), 201



if __name__ == "__main__":
    app.run(debug=True)
