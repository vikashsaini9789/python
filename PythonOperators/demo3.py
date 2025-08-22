# Logical Operators

a = 10

# AND Operators
result = a > 5 and a < 20
print(result)

# OR Operators
result = a < 5 or a > 8
print(result)

# NOT Operators 
result  = not(a > 5 and a < 20)
print(result)

str = "GFG"
print(not (not(str and "")))
