from flask import Flask, request

app = Flask(__name__)

emps = [
    {"id": 1, "name": "Rohit", "sal": 50000},
    {"id": 2, "name": "Aman", "sal": 60000},
    {"id": 3, "name": "Priya", "sal": 55000}
]

@app.get("/")
def home():
    return "Employee API"

@app.get("/emps")
def get_all_employees():
    return emps

@app.get("/emps/<int:emp_id>")
def get_employee(emp_id):
    for emp in emps:
        if emp["id"] == emp_id:
            return emp
    return {"message": "Employee not found"}, 404

@app.post("/emps")
def add_employee():
    emp = {
        "id": int(request.form["id"]),
        "name": request.form["name"],
        "sal": int(request.form["sal"])
    }

    emps.append(emp)
    return {"message": "Employee added successfully"}

@app.get("/search")
def search():
    name = request.args.get("name")

    result = []
    for emp in emps:
        if emp["name"].lower() == name.lower():
            result.append(emp)

    return result

@app.get("/application-info")
def application_info():
    return {
        "application": "Employee API",
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(debug=True)
