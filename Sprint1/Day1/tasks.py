# Variables
name = "Alice"
age = 25

# Function
def greet(user_name):
    print(f"Hello, {user_name}!")

# Loop
for i in range(3):
    print(f"Loop iteration: {i}")

# Class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

# Call the function
greet(name)

# Create an object and call its method
person1 = Person(name, age)
person1.introduce()
