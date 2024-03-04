#!/usr/bin/env python
import cgi
import subprocess

form = cgi.FieldStorage()

# Get user input from the HTML form
user_input = form.getvalue("input")

# Run your Python script with user input
result = subprocess.run(["python", "Linkage.py"], input=user_input.encode(), text=True, capture_output=True)

# Print the output
print("Content-type: text/plain\n")
print(result.stdout)
