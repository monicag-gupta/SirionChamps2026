from flask import Flask,request,render_template,redirect,url_for,abort

app = Flask(__name__)

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
    return "Display all employees"

@app.post("/emps")
def add_employee():
    return "Create an employee"

@app.route("/employee/<name>")
def employee_by_name(name):
    return f"Employee name: {name}"

dict=[{
    'name':'Alice','salary':85000},
      {"name": "Bob Jones", "salary": 62000},
    {"name": "Charlie Brown", "salary": 74000}
]

@app.get('/dict')
def get_empl():
    return dict

@app.post('/dict/<name>/<sal>')
def add_emp(name,sal):
    d={'name':name,'sal':sal}
    dict.append(d)
    return 'Employee created'

@app.route("/department/<path:department_name>")
def department(department_name):
    return f"Department: {department_name}"

@app.route("/empl/<int:empl_id>")
def employee_by_id(employee_id):
    return f"Employee ID: {employee_id}"

@app.route("/salary/<float:amount>")
def salary(amount):
    return f"Employee salary: {amount}"



