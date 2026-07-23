# # from flask import Flask
# # app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return "Welcome to Flask!"

# # if __name__ == "__main__":
# #     app.run(debug=True)





# # from flask import Flask

# # app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return "Home Page"

# # @app.route("/about")
# # def about():
# #     return "About Us"

# # @app.route("/contact")
# # def contact():
# #     return "Contact Us"

# # @app.route("/employees")
# # def employees():
# #     return "Employee List"

# # if __name__ == "__main__":
# #     app.run(debug=True)'




# # from flask import Flask

# # app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return "Home Page"

# # @app.route("/about")
# # def about():
# #     return "About Us"

# # @app.route("/contact")
# # def contact():
# #     return "Contact Us"

# # @app.route("/employees")
# # def employees():
# #     return "Employee List"

# # @app.route("/employee", methods=["GET", "POST"])
# # def employee():
# #     return "Employee request received"


# # @app.get("/emps")
# # def get_employees():
# #     return "Display all employees"

# # @app.post("/emps")
# # def add_employee():
# #     return "Create an employee"

# # @app.route("/employee/<name>")
# # def employee_by_name(name):
# #     return f"Employee name: {name}"


# # if __name__ == "__main__":
# #     app.run(debug=True)



# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # In-memory database using a list of dictionaries
# employees_list = [
#     {"id": 1, "name": "Alice", "role": "Engineer"},
#     {"id": 2, "name": "Bob", "role": "Manager"}
# ]

# @app.route("/")
# def home():
#     return "Home Page"

# @app.route("/about")
# def about():
#     return "About Us"

# @app.route("/contact")
# def contact():
#     return "Contact Us"

# @app.route("/employees")
# def employees():
#     return "Employee List"

# @app.route("/employee", methods=["GET", "POST"])
# def employee():
#     return "Employee request received"


# # 1. GET method: Returns the list of dictionaries as JSON
# @app.get("/emps")
# def get_employees():
#     return jsonify(employees_list)


# # 2. POST method: Adds an employee via JSON request body
# @app.post("/emps")
# def add_employee():
#     data = request.get_json()
    
#     # Basic validation
#     if not data or not data.get("name") or not data.get("role"):
#         return jsonify({"error": "Please provide 'name' and 'role' in JSON body"}), 400
        
#     new_employee = {
#         "id": len(employees_list) + 1,
#         "name": data["name"],
#         "role": data["role"]
#     }
    
#     employees_list.append(new_employee)
#     return jsonify({"message": "Employee added successfully", "employee": new_employee}), 201


# # 3. Add via URL: Uses dynamic path parameters to add an employee via a GET request
# @app.route("/add_via_url/<string:name>/<string:role>")
# def add_employee_via_url(name, role):
#     new_employee = {
#         "id": len(employees_list) + 1,
#         "name": name,
#         "role": role
#     }
    
#     employees_list.append(new_employee)
#     return jsonify({"message": "Employee added via URL successfully", "employee": new_employee}), 201


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, jsonify

app = Flask(__name__)

# List of employee dictionaries
employees_list = [
    {"id": 1, "name": "Alice", "sal": "75000"},
    {"id": 2, "name": "Bob", "sal": "80000"}
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


# GET method: Returns the list of employee dictionaries
@app.get("/emps")
def get_employees():
    return jsonify(employees_list)


# POST method: Adds an employee using parameters from the URL
@app.post("/emps/<string:name>/<string:sal>")
def add_employee_url(name, sal):
    new_employee = {
        "id": len(employees_list) + 1,
        "name": name,
        "sal": sal
    }
    
    employees_list.append(new_employee)
    return jsonify({
        "message": "Employee added successfully!", 
        "employee": new_employee
    }), 201


if __name__ == "__main__":
    app.run(debug=True)