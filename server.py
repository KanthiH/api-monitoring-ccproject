from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Create a counter metric
API_REQUESTS = Counter('api_requests_total', 'Total API Requests')

@app.route('/')
def index():
    return "Welcome to the API Monitoring App!"

@app.route('/api')
def api():
    API_REQUESTS.inc()
    return {"message": "API request received!"}

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
