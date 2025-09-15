import tkinter as tk
import math, re

# ----------------------------
# Angle mode
# ----------------------------
mode = "DEG"

# ----------------------------
# Helpers
# ----------------------------
def format_number(n):
    if isinstance(n, (int, float)):
        n = round(n, 10)
        return int(n) if n.is_integer() else n
    return n

def _replace_constants(expr):
    expr = expr.replace("π", "math.pi")
    expr = re.sub(r'(?<![\w.])e(?![\w.])', 'math.e', expr)
    return expr

def _replace_functions(expr, angle_mode):
    if angle_mode == "DEG":
        expr = re.sub(r'asin\(', 'math.degrees(math.asin(', expr)
        expr = re.sub(r'acos\(', 'math.degrees(math.acos(', expr)
        expr = re.sub(r'atan\(', 'math.degrees(math.atan(', expr)
        expr = re.sub(r'sin\(', 'math.sin(math.radians(', expr)
        expr = re.sub(r'cos\(', 'math.cos(math.radians(', expr)
        expr = re.sub(r'tan\(', 'math.tan(math.radians(', expr)
    else:
        expr = re.sub(r'asin\(', 'math.asin(', expr)
        expr = re.sub(r'acos\(', 'math.acos(', expr)
        expr = re.sub(r'atan\(', 'math.atan(', expr)
        expr = re.sub(r'sin\(', 'math.sin(', expr)
        expr = re.sub(r'cos\(', 'math.cos(', expr)
        expr = re.sub(r'tan\(', 'math.tan(', expr)

    expr = expr.replace("√", "math.sqrt")
    expr = re.sub(r'log\(', 'math.log10(', expr)
    expr = re.sub(r'ln\(', 'math.log(', expr)
    expr = re.sub(r'exp\(', 'math.exp(', expr)
    return expr

def _replace_percent_and_power(expr):
    expr = expr.replace("^", "**")
    expr = expr.replace("%", "/100")
    return expr

def _handle_implicit_multiplication(expr):
    expr = expr.replace(")(", ")*(")
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    expr = re.sub(r'\)(\d)', r')*\1', expr)
    return expr

def _replace_factorial(expr):
    expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)
    return expr

def get_internal_expr(display_expr):
    expr = display_expr.replace("×", "*").replace("÷", "/")
    expr = _replace_percent_and_power(expr)
    expr = _replace_constants(expr)
    expr = _replace_functions(expr, mode)
    expr = _replace_factorial(expr)
    expr = _handle_implicit_multiplication(expr)
    return expr

def safe_eval(expr):
    try:
        return format_number(eval(expr, {"__builtins__": None, "math": math}, {}))
    except:
        return ""

# ----------------------------
# Events
# ----------------------------
def update_result():
    current = entry.get()
    if current.strip() == "":
        result_var.set("")
        return
    result_var.set(safe_eval(get_internal_expr(current)))

def on_click(symbol):
    current = entry.get()
    if symbol == "=":
        if result_var.get() != "":
            entry.delete(0, tk.END)
            entry.insert(0, result_var.get())
        return
    elif symbol == "AC":
        entry.delete(0, tk.END)
        result_var.set("")
        return
    elif symbol == "⌫":
        entry.delete(0, tk.END)
        entry.insert(0, current[:-1])
        update_result()
        return
    elif symbol == "()":
        if current.count("(") == current.count(")"):
            entry.insert(tk.END, "(")
        else:
            entry.insert(tk.END, ")")
    elif symbol == "x²":
        entry.insert(tk.END, "^2")
    elif symbol == "xʸ":
        entry.insert(tk.END, "^")
    else:
        if symbol == "*": symbol = "×"
        elif symbol == "/": symbol = "÷"
        entry.insert(tk.END, symbol)
    update_result()

def set_mode(new_mode):
    global mode
    mode = new_mode
    if mode == "DEG":
        deg_button.config(bg="#fbbc05", fg="black")
        rad_button.config(bg="#5f6368", fg="white")
    else:
        rad_button.config(bg="#fbbc05", fg="black")
        deg_button.config(bg="#5f6368", fg="white")
    update_result()

# ----------------------------
# UI Setup
# ----------------------------
root = tk.Tk()
root.title("Google-style Scientific Calculator")
root.configure(bg="#202124")
root.geometry("600x700")

for r in range(0, 12):
    root.grid_rowconfigure(r, weight=1)
for c in range(0, 6):
    root.grid_columnconfigure(c, weight=1)

# Input + result
entry = tk.Entry(root, font=("Arial", 28), bd=0, justify="right",
                 bg="#303134", fg="white")
entry.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)
entry.focus()

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Arial",16),
                        anchor="e", bg="#202124", fg="#34a853")
result_label.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=10)

btn_style = {"font":("Arial",16), "bd":0, "relief":"flat", "width":5, "height":2}

def make_button(text, row, col, bg, fg="white", colspan=1):
    b = tk.Button(root, text=text, bg=bg, fg=fg,
                  command=lambda: on_click(text), **btn_style)
    b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
    return b

# DEG / RAD toggle
deg_button = tk.Button(root, text="DEG", command=lambda: set_mode("DEG"),
                       bg="#fbbc05", fg="black", **btn_style)
deg_button.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=3, pady=3)

rad_button = tk.Button(root, text="RAD", command=lambda: set_mode("RAD"),
                       bg="#5f6368", fg="white", **btn_style)
rad_button.grid(row=2, column=3, columnspan=3, sticky="nsew", padx=3, pady=3)

# Button Layout
buttons = [
    ["AC", "()", "%", "÷", "√", "x²"],
    ["7", "8", "9", "×", "sin", "cos"],
    ["4", "5", "6", "-", "tan", "log"],
    ["1", "2", "3", "+", "ln", "exp"],
    ["0", ".", "⌫", "=", "π", "e"],
    ["xʸ", "!", "asin", "acos", "atan", ""]
]

for r, row in enumerate(buttons, 3):
    for c, s in enumerate(row):
        if not s: continue
        color = "#3c4043"
        if s in ["+","-","×","÷","%","x²","xʸ"]: color = "#5f6368"
        if s == "=": color = "#4285F4"
        if s == "AC": color = "#EA4335"
        if s == "⌫": color = "#6c757d"
        make_button(s, r, c, color)

root.mainloop()
