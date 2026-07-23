from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

app = Flask(__name__)

# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================
# Update these variables with your actual MySQL credentials
db_user = "root"
db_password = "rajEnDer@561770" # It is now safe to use @, #, etc.
db_host = "localhost"
db_name = "employee_db"

# Safely encode the password for the connection string
encoded_password = quote_plus(db_password)

# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# ==========================================
# 2. DATABASE MODEL
# ==========================================
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    # Helper method to convert the object to a dictionary for JSON responses
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "role": self.role
        }

# Create the tables in the database before the first request
with app.app_context():
    db.create_all()

# ==========================================
# 3. API ROUTES
# ==========================================

# 1. GET / - Display the application name
@app.route('/', methods=['GET'])
def index():
    return jsonify({"application_name": "Employee Information API (MySQL Edition)"})

# 2. GET /employees - Display all employees
@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

# 3. GET /employees/<employee_id> - Display one employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = db.session.get(Employee, employee_id)
    if employee:
        return jsonify(employee.to_dict())
    
    return jsonify({"error": "Employee not found"}), 404

# 4. POST /employees - Add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    
    # Basic validation
    required_fields = ["name", "department", "role"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
    
    # Check if ID was provided manually and if it already exists
    if "id" in data:
        existing_emp = db.session.get(Employee, data["id"])
        if existing_emp:
            return jsonify({"error": "Employee with this ID already exists"}), 400
        new_employee = Employee(id=data["id"], name=data["name"], department=data["department"], role=data["role"])
    else:
        # Let MySQL auto-increment the ID
        new_employee = Employee(name=data["name"], department=data["department"], role=data["role"])
        
    db.session.add(new_employee)
    db.session.commit()
    
    return jsonify(new_employee.to_dict()), 201

# 5. GET /search - Search employees by department
@app.route('/search', methods=['GET'])
def search_employees():
    department = request.args.get('department')
    
    if not department:
        return jsonify({"error": "Please provide a 'department' query parameter"}), 400
        
    # Case-insensitive search using SQLAlchemy's ilike
    employees = Employee.query.filter(Employee.department.ilike(f"{department}")).all()
    
    if not employees:
         return jsonify([]), 200
         
    return jsonify([emp.to_dict() for emp in employees])

# 6. GET /application-info - Return a custom response
@app.route('/application-info', methods=['GET'])
def get_app_info():
    content = {
        "status": "Healthy",
        "version": "2.0.0",
        "framework": "Flask",
        "database": "MySQL",
        "description": "API for managing internal employee records."
    }
    
    response = make_response(jsonify(content), 200)
    response.headers["X-Custom-System"] = "Employee-Tracking"
    return response

if __name__ == '__main__':
    app.run(debug=True)