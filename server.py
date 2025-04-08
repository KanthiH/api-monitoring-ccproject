from flask import Flask, jsonify, request
import logging
from multiprocessing import Process

def create_app_single_route(route_name):
    app = Flask(__name__)
    logger = logging.getLogger(f"{route_name.upper()}_LOGGER")
    logging.basicConfig(level=logging.INFO)

    if route_name == "ping":
        @app.route("/ping", methods=["GET"])
        def ping():
            logger.info("Ping called")
            return jsonify({"message": "pong"}), 200

    elif route_name == "hello":
        @app.route("/hello", methods=["GET"])
        def hello():
            logger.info("Hello endpoint hit")
            return jsonify({"message": "Hello, World!"}), 200

    elif route_name == "add":
        @app.route("/add", methods=["POST"])
        def add():
            data = request.json
            result = data.get("a", 0) + data.get("b", 0)
            logger.info(f"Add called with: {data}")
            return jsonify({"result": result})

    elif route_name == "status":
        @app.route("/status", methods=["GET"])
        def status():
            logger.info("Status checked")
            return jsonify({"status": "ok"})

    elif route_name == "echo":
        @app.route("/echo", methods=["POST"])
        def echo():
            data = request.json
            logger.info(f"Echo data: {data}")
            return jsonify({"you_sent": data})

    return app

def run_app(route_name, port):
    app = create_app_single_route(route_name)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    routes_ports = {
        "ping": 5000,
        "hello": 5001,
        "add": 5002,
        "status": 5003,
        "echo": 5004,
    }

    processes = []
    for route, port in routes_ports.items():
        p = Process(target=run_app, args=(route, port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
