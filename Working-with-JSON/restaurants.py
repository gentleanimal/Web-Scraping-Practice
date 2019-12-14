"""Open your json file using 'with' so it will automatically close the file.
Load file into a variable. Determine what info you want by the keys.
Create empty list for each of the keys and determine where those keys are
in the json file. Look at line 24, it has the location of the keys you are looking
for stored in the var rest. Utilize the print statement to verify whether you are
in a List or Dict and drill down to exact location of the info you need. The
integer in the [ ] is the position of the element in a list. This then shows that
that element begins a Dict and so on."""

import json
from pprint import pprint

with open('restaurants.json', 'r') as file:
    data = json.load(file)
keys = ['id', 'name']
n = 0
id = []
name = []
# The following print statements are just to show the steps needed.
print(type(data['explore_tabs']))
print(type(data['explore_tabs'][0]))
print(type(data['explore_tabs'][0]['sections']))
print(type(data['explore_tabs'][0]['sections'][0]))
print(type(data['explore_tabs'][0]['sections'][0]['point_of_interest_items']))

rest = data['explore_tabs'][0]['sections'][0]['point_of_interest_items']

for n in range(len(rest)):
    ids = data['explore_tabs'][0]['sections'][0]['point_of_interest_items'][n]['id']
    names = data['explore_tabs'][0]['sections'][0]['point_of_interest_items'][n]['name']
    id.append(ids)
    name.append(names)
eateries = dict(zip(id, name))  # Create a Dict from two lists, id and name

pprint(eateries) # Using pprint formats it as key, value and a new line
