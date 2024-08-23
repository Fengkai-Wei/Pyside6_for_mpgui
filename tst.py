# Original dictionary
dict_0 = {'name': 'Alice', 'age': 30}

# Assign dict_0 to another variable
a = dict_0

# Remove a key using pop
a.pop('age')

print(dict_0)  # Output: {'name': 'Alice'}
print(a)       # Output: {'name': 'Alice'}
print(a == dict_0)