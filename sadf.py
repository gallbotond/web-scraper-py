import re

s = "3.736,93 Lei"
match = re.search(r'\d.*\d', s)
if match:
    result = match.group()
    print(result)  # Outputs: 123 some text 456 more text 789