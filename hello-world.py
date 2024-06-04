from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    link_to_hello = f"""
    <a href="{url_for('hello', username='Ansellma')}">Link</a>
    """
    return link_to_hello

@app.route('/hello/')
@app.route("/hello/<username>")
def hello(username=None):
    return render_template('dummy/hello.html', username=username)

# Make sure all routes are defined before creating the test request context
with app.test_request_context():
    print(url_for('index'))  # Output: /
    print(url_for('hello', username='John Doe'))  # Output: /hello/John%20Doe

if __name__ == "__main__":
    app.run(debug=True)
