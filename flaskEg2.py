from flask import Flask, jsonify

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

@app.route("/employees")
def employees():
    return "Employee List"

@app.route("/employee", methods=["GET", "POST"])
def employee():
    return "Employee request received"

@app.get("/emps")
def get_employees():
    return EMPLOYEES

@app.post("/emps")
def add_employee():
    return "Create an employee"

@app.route("/employee/<name>")
def employee_by_name(name):
    matching_employees = [
        emp for emp in EMPLOYEES 
        if emp["name"].lower() == name.lower()
    ]
    if not matching_employees:
        return jsonify({"status": "error", "message": f"No employee found with name '{name}'"}), 404
        
    return jsonify({"status": "success", "data": matching_employees})


# FIXED: Changed <emp_id:int> to <int:emp_id> for Flask syntax
@app.post("/employee/<name>/<int:emp_id>")
def employee_by_name_and_id(name, emp_id):
    # Filter by BOTH name and ID
    matching_employees = [
        emp for emp in EMPLOYEES 
        if emp["id"] == emp_id and emp["name"].lower() == name.lower()
    ]
    
    if not matching_employees:
        return jsonify({
            "status": "error", 
            "message": f"No employee found with name '{name}' and ID '{emp_id}'"
        }), 404
    
    return jsonify({"status": "success", "data": matching_employees})

if __name__ == "__main__":
    app.run(debug=True)