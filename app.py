from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return f"Hello from demo-app, version {os.getenv('APP_VERSION', 'dev')}\n"

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
