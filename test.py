#This is used to test the calculatorJavaLib

from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

calculator = gateway.entry_point.getCalculator()

print("Addition:", calculator.add(10.0, 20.0))
print("Subtraction:", calculator.subtract(20.0, 5.0))
print("Multiplication:", calculator.multiply(6.0, 7.0))
print("Division:", calculator.divide(20.0, 4.0))

gateway.close()
