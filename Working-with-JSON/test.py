import json
import pprint

with open('employees.json', 'r') as file:
    data = json.load(file)


printer = pprint.PrettyPrinter()
# printer.pprint(data)

language = data.get('programming_language')

employees = data.get('employees')

print(language)

for employee in employees:
    print(employee.get('id'), employee.get('fullname'))
