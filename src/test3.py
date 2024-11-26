import re

def contains_number(s):
    # Search for any digits in the string
    return bool(re.search(r'\d', s))

# Example usage
string = "Hello"
print(contains_number(string))  # Output: True
