import tkinter as tk
import re

# ----------------------------
# Helper Functions
# ----------------------------

def format_number(n):
    """Format numbers nicely"""
    if isinstance(n, (int, float)):
        if isinstance(n, float):
            n = round(n, 8)
            return int(n) if n.is_integer() else n
        return n
    return n

def get_internal_expr(display_expr):
    """Convert display expression (× ÷ %) to Python eval"""
    expr = display_expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("%", "/100")
    expr = expr.replace(")(", ")*(")
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    expr = re.sub(r'\)(\d)', r')*\1', expr)
    return expr

def safe_eval(expr):
    """Safely evaluate expression for live result"""
    try:
        return format_number(eval(expr))
    except:
        return ""

# ----------------------------
# Event Handlers
# ----------------------------

def update_result():
    """Show live result in the entry"""
    current = entry.get()
    if current.strip() == "":
        result_var.set("")
        return
    internal_expr = get_internal_expr(current)
    result_var.set(safe_eval(internal_expr))

def on_click(symbol):
    """Handle button clicks"""
    current = entry.get()
    
    if symbol == "=":
        # Move live result to entry
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
        update_result()
        return

    else:
        if symbol == "*":
            symbol = "×"
        elif symbol == "/":
            symbol = "÷"

        if current and current[-1] in "+-×÷%" and symbol in "+-×÷%":
            entry.delete(len(current)-1, tk.END)

        entry.insert(tk.END, symbol)
        update_result()

def on_key(event):
    """Handle keyboard input"""
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
        if result_var.get() != "":
            entry.delete(0, tk.END)
            entry.insert(0, result_var.get())
    elif key == "BackSpace":
        entry.delete(len(entry.get())-1, tk.END)
    elif key == "Escape":
        entry.delete(0, tk.END)
        result_var.set("")
    update_result()
    return "break"      #prevent double key insertion

# ----------------------------
# Hover and Press Effects
# ----------------------------

def lighten_color(color, factor=1.2):
    color = color.lstrip('#')
    r = min(int(int(color[0:2],16)*factor),255)
    g = min(int(int(color[2:4],16)*factor),255)
    b = min(int(int(color[4:6],16)*factor),255)
    return f'#{r:02x}{g:02x}{b:02x}'

def on_enter(e):
    e.widget.configure(bg=lighten_color(e.widget.original_bg, 1.2))

def on_leave(e):
    e.widget.configure(bg=e.widget.original_bg)

def on_press(e):
    e.widget.configure(relief="sunken")
    e.widget.after(100, lambda: e.widget.configure(relief="ridge"))

# ----------------------------
# Main Window Setup
# ----------------------------

root = tk.Tk()
root.title("Live Calculator")
root.configure(bg="white")

# Make window resizable
root.rowconfigure(0, weight=1)
for i in range(1,6):
    root.rowconfigure(i, weight=1)
for j in range(4):
    root.columnconfigure(j, weight=1)

# Entry
entry = tk.Entry(root, font=("Arial", 24), bd=5, relief="ridge",
                 justify="right", bg="white", fg="black")
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
entry.focus()

# Live result variable
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Arial",14), anchor="e", bg="white", fg="green")
result_label.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=(0,5))

# Buttons
buttons = [
    ["AC", "()", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="]
]

btn_style = {"font":("Arial",18), "bd":1, "relief":"ridge"}

button_refs = {}
for r, row in enumerate(buttons,2):
    for c,symbol in enumerate(row):
        btn = tk.Button(root, text=symbol, command=lambda s=symbol: on_click(s), **btn_style)
        btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
        button_refs[btn] = symbol
        if symbol=="AC":
            btn.configure(bg="#d9534f", fg="white")
        elif symbol=="=":
            btn.configure(bg="#0275d8", fg="white")
        elif symbol in ["+","-","×","÷","%"]:
            btn.configure(bg="#5bc0de", fg="white")
        elif symbol=="⌫":
            btn.configure(bg="#6c757d", fg="white")
        else:
            btn.configure(bg="#f0f0f0", fg="black")
        btn.original_bg = btn.cget("bg")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_press)

entry.bind("<KeyPress>", on_key)

root.mainloop()

