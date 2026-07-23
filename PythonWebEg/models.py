class Employee:
    def __init__(self, id, name, salary):
        self.id = id
        self.name = name
        self.salary = salary

    def to_dict(self):
        return {"id": self.id, "name": self.name, "salary": self.salary}
