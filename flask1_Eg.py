from flask import Flask

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



if __name__ == "__main__":
    app.run(debug=True)
