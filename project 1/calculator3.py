import math

# helper function to format numbers nicely
def format_number(n):
    if isinstance(n, (int, float)):
        return int(n) if isinstance(n, float) and n.is_integer() else n
    return n


def calculator():
    print("🔢 Scientific Calculator (type 'exit' to quit)")
    print("Available functions: +, -, *, /, ^, %, sqrt(x), sin(x), cos(x), tan(x), log(x), exp(x)")
    print("Constants: pi, e")

    while True:
        expr = input("\nEnter expression: ")

        if expr.lower() in ['exit', 'quit']:
            print("Exiting Calculator. Goodbye!")
            break

        try:
            # replace ^ with ** for power
            expr = expr.replace("^", "**")

            # allow only safe characters
            allowed_chars = "0123456789+-*/.%()eE "  
            extra_allowed = ["sqrt", "sin", "cos", "tan", "log", "exp", "pi", "e"]
            if not all(c.isalnum() or c in allowed_chars for c in expr.replace(" ", "")):
                if not any(func in expr for func in extra_allowed):
                    print("Error: Invalid characters detected!")
                    continue

            # safe eval environment
            safe_dict = {k: getattr(math, k) for k in ["sqrt", "sin", "cos", "tan", "log", "exp", "pi", "e"]}
            safe_dict.update({"__builtins__": None})  # disable unsafe stuff

            # evaluate
            result = eval(expr, safe_dict, {})
            print(f"{expr} = {format_number(result)}")

        except ZeroDivisionError:
            print("Error! Division by zero.")
        except Exception as e:
            print("Invalid expression! Try again.")


# Run calculator
calculator()
