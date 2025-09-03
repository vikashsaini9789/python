# Python program to create a simple calculator

# helper function to format numbers nicely
def format_number(n):
    if isinstance(n, (int, float)):
        return int(n) if isinstance(n, float) and n.is_integer() else n
    return n              # for error messages like divide by zero


# step 2 & 3: user input + print result
def calculator():
    print("Simple Calculator (type 'exit' to quit)")
    while True:
        expr = input("\nEnter expression (e.g., 3 * 4): ")

        if expr.lower() in ['exit', 'quit']:
            print("Exiting Calculator. Goodbye!")
            break

        try:
            # allow only safe characters
            allowed_chars = "0123456789+-*/.() "
            if not all(c in allowed_chars for c in expr):
                print("Error: Invalid characters detected!")
                continue

            # evaluate the math expression
            result = eval(expr)
            print(f"{expr} = {format_number(result)}")

        except ZeroDivisionError:
            print("Error! Division by zero.")
        except Exception:
            print("Invalid expression! Try again.")


# Run calculator
calculator()
