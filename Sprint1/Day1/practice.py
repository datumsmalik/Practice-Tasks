import json
import csv

#list
fruits = ["apple", "banana", "cherry"]
print("Original list:", fruits)

# Add and remove items
fruits.append("orange")
fruits.remove("banana")
print("Updated list:", fruits)

# Loop over list
for fruit in fruits:
    print("I like", fruit)

#dictionaries
person = {"name": "Alice", "age": 30, "city": "New York"}
print("\nOriginal dict:", person)

# Add and update keys
person["email"] = "alice@example.com"
person["age"] = 31
print("Updated dict:", person)

# Loop over dict
for key, value in person.items():
    print(f"{key}: {value}")

#read write jsin
# Write dict to JSON file
with open("data.json", "w") as json_file:
    json.dump(person, json_file)

# Read JSON back into Python
with open("data.json", "r") as json_file:
    data_from_json = json.load(json_file)

print("\nLoaded from JSON:", data_from_json)

#csv file read and write
# Data to write
people = [
    ["name", "age", "city"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]

# Write CSV file
with open("people.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(people)

# Read CSV file
with open("people.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    print("\nCSV contents:")
    for row in reader:
        print(row)
