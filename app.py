from flask import Flask, render_template_string, request
import secrets, string

app = Flask(__name__)

def generate_password(length=16, use_upper=True, use_digits=True, use_symbols=True):
    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>/?~"
    return ''.join(secrets.choice(chars) for _ in range(length))

HTML = """
<!doctype html>
<html>
  <head><title>Password Generator</title></head>
  <body style="font-family:sans-serif;">
    <h1>Secure Password Generator</h1>
    <form method="post">
      Length: <input type="number" name="length" value="16" min="8" max="64"><br>
      <label><input type="checkbox" name="upper" checked> Uppercase</label><br>
      <label><input type="checkbox" name="digits" checked> Digits</label><br>
      <label><input type="checkbox" name="symbols" checked> Symbols</label><br>
      <button type="submit">Generate</button>
    </form>
    {% if password %}
      <h2>Your Password:</h2>
      <p style="font-family:monospace;">{{ password }}</p>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    if request.method == "POST":
        length = int(request.form.get("length", 16))
        use_upper = "upper" in request.form
        use_digits = "digits" in request.form
        use_symbols = "symbols" in request.form
        password = generate_password(length, use_upper, use_digits, use_symbols)
    return render_template_string(HTML, password=password)

if __name__ == "__main__":
    app.run(debug=True)
