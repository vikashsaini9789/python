#python program to create a simple calculator

# Here i'm using 3 steps to build calculator program :-
# 1. functions for operations
# 2. user input
# 3. print result


#step 1: creating functions :-

# function to add two numbers
def add(*numbers):
    return sum(numbers)

# function to subtract two numbers
def subtract(*numbers):
    if not numbers:          # if no numbers passed
        return 0
    result = numbers[0]      # start with the first number
    for n in numbers[1:]:
        result -= n
    return result 

# function to multiply two numbers
def multiply(*numbers):
    result = 1
    for num in numbers:
        result *= num
    return result 

# function to divide two numbers
def divide(*numbers):
    if not numbers:
        return None          # no numbers passed
    result = numbers[0]
    for n in numbers[1:]:
        if n == 0:
            print("Warning: Skipping division by zero.")
            continue
        result /= n
    return result

# function to find average of numbers
def average(*numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

# helper function to format numbers nicely
def format_number(n):
    if isinstance(n, (int, float)):
        return int(n) if isinstance(n, float) and n.is_integer() else n 
    return n              # for error messages like divide by zero


# step 2: user input :-

def calculator():
    while True:
        print("\nSelect operation:\n"
            "  1. Addition\n"
            "  2. Subtraction\n"
            "  3. Multiplication\n"
            "  4. Division\n"
            "  5. Average")

        try:
            select = int(input("Select an operation (1-5): "))
        except ValueError:
            print("Invalid input! Please enter a number between 1-5.")
            continue

        raw_numbers = input("Enter numbers (integers or decimals) seprated by space: ").split()

        if not raw_numbers:         # prevent crash
            print("No numbers entered! Try again.")
            continue

# convert to int if possible, else float
        numbers = [float(n) if "." in n else int(n) for n in raw_numbers]
   

# step 3: print result :- 

        if select == 1:
            result = add(*numbers)
            print(f"{' + '.join(map(str, numbers))} = {format_number(result)}")

        elif select == 2:
            result = subtract(*numbers)
            print(f"{' - '.join(map(str, numbers))} = {format_number(result)}")

        elif select == 3:
            result = multiply(*numbers)
            print(f"{' * '.join(map(str, numbers))} = {format_number(result)}")

        elif select == 4:
            result = divide(*numbers)
            print(f"{' / '.join(map(str, numbers))} = {format_number(result)}")

        elif select == 5:
            result = average(*numbers)
            if len(numbers) == 1:
                print(f"{numbers[0]} / 1 = {format_number(result)}")
            else:
                print(f"({' + '.join(map(str, numbers))}) / {len(numbers)} = {format_number(result)}")

        else:
            print("Invalid operation ! please select between 1-5.")

#continue or exit 
        choice = input("\nDo you want to continue? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting Calculator. Goodbye!")
            break 


# Run calculator
calculator()
