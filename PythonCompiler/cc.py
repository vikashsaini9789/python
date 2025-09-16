from flask import Flask, render_template_string, request, jsonify
import io
import traceback
from multiprocessing import Process, Queue
import builtins

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Online Compiler</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { font-size: 24px; margin-bottom: 20px; }
        #editor { height: 300px; width: 100%; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; line-height: 1.5; }
        #user_input { width: 100%; height: 100px; margin-top: 10px; font-size: 14px; }
        button { font-size: 16px; padding: 10px 20px; margin-top: 10px; cursor: pointer; border: none; border-radius: 4px; background-color: #007bff; color: white; }
        button:hover { background-color: #0056b3; }
        pre { font-size: 14px; background-color: #282c34; color: #abb2bf; padding: 15px; border: 1px solid #444; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; overflow: auto; }
        #loading { display: none; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Python Online Compiler</h1>
    <div id="editor"></div>
    <textarea id="user_input" placeholder="Enter input here, each line for each input() call..."></textarea>
    <button onclick="runCode()">Run Code</button>
    <div id="loading">Running...</div>
    <pre id="output"></pre>

    <script>
    const editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");

    // Editor setup
    editor.setOptions({
        fontSize: "14pt",
        showPrintMargin: false,
        wrap: true,
    });
    editor.resize();
    editor.focus();

    async function runCode() {
        document.getElementById('output').textContent = '';
        document.getElementById('loading').style.display = 'block';

        const code = editor.getValue();
        const userInput = document.getElementById('user_input').value;

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, input: userInput })
            });

            const result = await response.json();
            let outputText = '';

            if (result.output) outputText += "Output:\\n" + result.output;
            if (result.error) outputText += "\\nError:\\n" + result.error;

            document.getElementById('output').textContent = outputText;
        } catch (err) {
            document.getElementById('output').textContent = "Error:\\n" + err;
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)


def run_user_code(code, user_input, queue):
    """Run user code with captured output and safe builtins."""
    output_buffer = io.StringIO()
    try:
        input_iter = iter(user_input)

        # Custom print and input
        def custom_input(prompt=None):
            try:
                return next(input_iter)
            except StopIteration:
                raise EOFError("EOF when reading a line")
            
        safe_builtins = {
            'abs': abs, 'len': len, 'range': range, 'int': int, 'float': float, 'str': str,
            'bool': bool, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
            'enumerate': enumerate, 'sum': sum, 'min': min, 'max': max,
            'any': any, 'all': all, 'zip': zip, 'sorted': sorted
        }

        local_env = {
            '__builtins__': safe_builtins,
            'input': custom_input,
            'print': lambda *args, **kwargs: print(*args, **kwargs, file=output_buffer)
        }

        exec(code, {}, local_env)
        queue.put({'output': output_buffer.getvalue()})
    except Exception:
        queue.put({'error': traceback.format_exc()})
    finally:
        output_buffer.close()


@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400

    code = data['code']
    user_input = data.get('input', '').splitlines()
    queue = Queue()

    p = Process(target=run_user_code, args=(code, user_input, queue))
    p.start()
    p.join(timeout=5)  # timeout protection

    if p.is_alive():
        p.terminate()
        return jsonify({'error': 'Execution timed out'}), 408

    result = queue.get() if not queue.empty() else {}
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=1010)
