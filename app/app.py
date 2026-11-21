from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    version = os.getenv("APP_VERSION", "v1")
    pod = socket.gethostname()
    return f"""

    <html>
      <head><title>AutoShip CI/CD</title></head>
      <body style="margin:0;height:100vh;display:flex;flex-direction:column;
                   justify-content:center;align-items:center;text-align:center;
                   font-family:Arial;background:#0f172a;color:#e2e8f0">
        <h1>🚀 AutoShip CI/CD Pipeline</h1>
        <p>GitHub → Jenkins (AWS EC2) → Docker Hub → Kubernetes (GKE)</p>
        <p>Version: <b>{version}</b></p>
      </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)