from flask import Flask, render_template_string, request, jsonify
import os
import subprocess
import sys

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Compiler</title>	
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { font-size: 24px; margin-bottom: 20px; }
        #editor { height: 300px; width: 100%; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; line-height: 1.5; }
        #user_input { width: 100%; height: 100px; margin-top: 10px; font-size: 14px; }
        button { font-size: 16px; padding: 10px 20px; margin-top: 10px; cursor: pointer; border: none; border-radius: 4px; background-color: #007bff; color: white; }
        button:hover { background-color: #0056b3; }
        pre { font-size: 14px; background-color: #282c34; color: #abb2bf; padding: 15px; border: 1px solid #444; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; overflow: auto; }
    </style>
</head>
<body>
    <h1>Python Online Compiler</h1>
    <div id="editor"></div>
    <textarea id="user_input" placeholder="Enter input here, each line for each input() call..."></textarea>
    <button onclick="runCode()">Run Code</button>
    <pre id="output"></pre>

    <script>
        const editor = ace.edit("editor");
        editor.setTheme("ace/theme/monokai");
        editor.session.setMode("ace/mode/python");

        async function runCode() {
            const code = editor.getValue();
            const userInput = document.getElementById('user_input').value;
            
            const response = await fetch('/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, input: userInput })
            });

            const result = await response.json();
            document.getElementById('output').textContent =
                (result.output || '') + (result.error ? '\\nError:\\n' + result.error : '');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({'error': 'Invalid code'}), 400

    code = data['code']
    user_input = data.get('input', '')
    file_path = os.path.join(os.getcwd(), 'temp_code.py')

    try:
        # Preprocess code to remove input prompts
        wrapper_code = f"""
import builtins
import sys

# override input to ignore prompts
input_lines = iter({user_input.splitlines()!r})
def input(prompt=None):
    try:
        return next(input_lines)
    except StopIteration:
        raise EOFError("No more input provided.")

{code}
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)

        # Execute code
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        os.remove(file_path)

        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'output': result.stdout, 'error': result.stderr}), 400

    except subprocess.TimeoutExpired:
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': 'Execution timed out'}), 408
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=1010)
