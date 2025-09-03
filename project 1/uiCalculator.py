import tkinter as tk
import re

# helper function to format numbers nicely
def format_number(n):
    if isinstance(n, (int, float)):
        return int(n) if isinstance(n, float) and n.is_integer() else n
    return n

def get_internal_expr(display_expr):
    """Convert pretty display expression to valid Python eval expression"""
    expr = display_expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("%", "/100")  # percentage
    expr = expr.replace(")(", ")*(")  # (2)(3) -> (2)*(3)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)   # 4(2) -> 4*(2)
    expr = re.sub(r'\)(\d)', r')*\1', expr)   # (2)3 -> (2)*3
    return expr

def on_click(symbol):
    if symbol == "=":
        expr = entry.get()
        try:
            internal_expr = get_internal_expr(expr)
            result = eval(internal_expr)
            result = format_number(result)

            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))

        except ZeroDivisionError:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error (Div by 0)")
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    elif symbol == "AC":
        entry.delete(0, tk.END)

    elif symbol == "⌫":
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, current[:-1])

    elif symbol == "()":  # auto-insert parentheses
        current = entry.get()
        if current.count("(") == current.count(")"):
            entry.insert(tk.END, "(")
        else:
            entry.insert(tk.END, ")")

    else:
        # Replace operators for display
        if symbol == "*":
            symbol = "×"
        elif symbol == "/":
            symbol = "÷"
        entry.insert(tk.END, symbol)

    entry.focus()


# Handle keyboard input
def on_key(event):
    key = event.keysym
    if key.isdigit() or key in ["parenleft", "parenright", "period"]:
        entry.insert(tk.END, event.char)
    elif key in ["plus", "minus"]:
        entry.insert(tk.END, event.char)
    elif key == "asterisk":
        entry.insert(tk.END, "×")
    elif key == "slash":
        entry.insert(tk.END, "÷")
    elif key == "percent":
        entry.insert(tk.END, "%")
    elif key == "Return":
        on_click("=")
    elif key == "BackSpace":
        on_click("⌫")
    elif key == "Escape":
        on_click("AC")


# Main window
root = tk.Tk()
root.title("Simple Calculator")
root.configure(bg="white")  # white theme

# Entry display
entry = tk.Entry(root, width=20, font=("Arial", 18), bd=5,
                 relief="ridge", justify="right", bg="white", fg="black")
entry.grid(row=0, column=0, columnspan=4, pady=5, padx=5)
entry.focus()

# Buttons layout
buttons = [
    ["AC", "()", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="]
]

# Button styles
btn_style = {
    "font": ("Arial", 16),
    "width": 5,
    "height": 2,
    "bd": 1,
    "relief": "ridge"
}

# Colors for white theme
colors = {
    "AC": {"bg": "#d9534f", "fg": "white"},   # red
    "=": {"bg": "#0275d8", "fg": "white"},    # dark blue
    "operators": {"bg": "#5bc0de", "fg": "white"},  # light blue
    "delete": {"bg": "#6c757d", "fg": "white"},     # gray
    "numbers": {"bg": "#f0f0f0", "fg": "black"}     # light gray
}

# Place buttons
for r, row in enumerate(buttons, 1):
    for c, symbol in enumerate(row):
        style = colors["numbers"]  # default

        if symbol == "AC":
            style = colors["AC"]
        elif symbol == "=":
            style = colors["="]
        elif symbol in ["+", "-", "×", "÷", "%"]:
            style = colors["operators"]
        elif symbol == "⌫":
            style = colors["delete"]

        tk.Button(root, text=symbol,
                  command=lambda s=symbol: on_click(s),
                  bg=style["bg"], fg=style["fg"], **btn_style).grid(row=r, column=c, padx=2, pady=2)

# Bind keyboard events
root.bind("<Key>", on_key)

root.mainloop()