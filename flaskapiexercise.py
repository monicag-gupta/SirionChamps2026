from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# In-memory database for demonstration purposes
employees_db = [
    {"id": 1, "name": "Alice Smith", "department": "Engineering", "role": "Backend Developer"},
    {"id": 2, "name": "Bob Jones", "department": "HR", "role": "HR Manager"},
    {"id": 3, "name": "Charlie Davis", "department": "Engineering", "role": "Frontend Developer"},
]

# 1. GET / - Display the application name
@app.route('/', methods=['GET'])
def index():
    return jsonify({"application_name": "Employee Information API"})

# 2. GET /employees - Display all employees
@app.route('/employees', methods=['GET'])
def get_all_employees():
    return jsonify(employees_db)

# 3. GET /employees/<employee_id> - Display one employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employees_db if emp["id"] == employee_id), None)
    if employee:
        return jsonify(employee)
    
    return jsonify({"error": "Employee not found"}), 404

# 4. POST /employees - Add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    new_employee = request.get_json()
    
    # Basic validation to ensure required fields exist
    required_fields = ["id", "name", "department", "role"]
    if not new_employee or not all(field in new_employee for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
    
    # Check if ID already exists
    if any(emp["id"] == new_employee["id"] for emp in employees_db):
        return jsonify({"error": "Employee with this ID already exists"}), 400
        
    employees_db.append(new_employee)
    return jsonify(new_employee), 201

# 5. GET /search - Search employees by department
@app.route('/search', methods=['GET'])
def search_employees():
    department = request.args.get('department')
    
    if not department:
        return jsonify({"error": "Please provide a 'department' query parameter"}), 400
        
    results = [emp for emp in employees_db if emp["department"].lower() == department.lower()]
    return jsonify(results)

# 6. GET /application-info - Return a custom response
@app.route('/application-info', methods=['GET'])
def get_app_info():
    content = {
        "status": "Healthy",
        "version": "1.0.0",
        "framework": "Flask",
        "description": "API for managing internal employee records."
    }
    
    # Using make_response allows you to add custom headers
    response = make_response(jsonify(content), 200)
    response.headers["X-Custom-System"] = "Employee-Tracking"
    return response

if __name__ == '__main__':
    app.run(debug=True)