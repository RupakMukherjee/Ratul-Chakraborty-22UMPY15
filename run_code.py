#!/usr/bin/env python
import cgi
import json
import subprocess

form = cgi.FieldStorage()

# Get user input from the HTML form
user_input = form.getvalue("input")

# Convert the input string to a Python list
input_data = json.loads(user_input)

# Run the Python script (linkage.py) with user input
result = subprocess.run(["python", "linkage.py"], input=json.dumps(input_data).encode(), text=True, capture_output=True)

# Print the output
print("Content-type: text/plain\n")
print(result.stdout)
