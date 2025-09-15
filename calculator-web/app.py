from flask import Flask, render_template, request, jsonify
import re, math

app = Flask(__name__, template_folder="templates")

# -------------------- Helpers --------------------
def format_number(n):
    if isinstance(n, (int, float)):
        if isinstance(n, float):
            n = round(n, 12)
            return int(n) if n.is_integer() else n
        return n
    return n

def get_internal_expr(display_expr):
    expr = display_expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    expr = expr.replace("√", "math.sqrt")
    expr = re.sub(r'(\d+(\.\d+)?)\%', r'(\1/100)', expr)
    expr = expr.replace(")(", ")*(")
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    expr = re.sub(r'\)(\d)', r')*\1', expr)
    expr = re.sub(r'(\d)(?=[a-zA-Z])', r'\1*', expr)
    expr = expr.replace("!", "math.factorial")
    return expr

def safe_eval(expr, mode="rad"):
    def make_trig(fn, inverse=False):
        if inverse:
            return (lambda x: math.degrees(fn(x))) if mode=="deg" else fn
        return (lambda x: fn(math.radians(x))) if mode=="deg" else fn

    safe_names = {
        "pi": math.pi, "e": math.e,
        "abs": abs, "round": round, "pow": pow, "sqrt": math.sqrt,
        "ln": math.log,
        "log": lambda x, base=10: math.log(x, base),
        "sin": make_trig(math.sin),
        "cos": make_trig(math.cos),
        "tan": make_trig(math.tan),
        "asin": make_trig(math.asin, inverse=True),
        "acos": make_trig(math.acos, inverse=True),
        "atan": make_trig(math.atan, inverse=True),
        "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
        "factorial": math.factorial
    }

    try:
        return format_number(eval(expr, {"__builtins__": None}, safe_names))
    except Exception:
        return ""

# -------------------- Routes --------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/calc", methods=["POST"])
def api_calc():
    data = request.get_json() or {}
    expr = data.get("expression", "")
    mode = data.get("mode", "rad")
    internal_expr = get_internal_expr(expr)
    result = safe_eval(internal_expr, mode)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
