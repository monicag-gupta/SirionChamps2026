with open("employee.txt", "w") as file:
    file.write("Employee ID,Name,Department,Salary\n")
    file.write("E001,Rahul Sharma,Training,45000\n")
    file.write("E002,Priya Nair,Human Resources,52000\n")
    file.write("E003,Amit Verma,Finance,60000\n")
    file.write("E004,Neha Singh,Operations,48000\n")
    file.write("E005,Karan Mehta,Information Technology,70000\n")

print("Employee data written successfully.")