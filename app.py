import os
import logging

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
)
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

metrics = PrometheusMetrics(app)
metrics.info("app_info", "Application information", version=os.getenv("APP_VERSION", "1.0.0"))


@app.route("/")
def index():
    logger.info("Root endpoint requested")
    return jsonify({
        "message": "Devps Cloud Project is running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/version")
def version():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0")
    })





@app.errorhandler(404)
def not_found(error):
    logger.warning("Resource not found", extra={"path": getattr(error, "description", None)})
    return jsonify({
        "error": "Not found"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    logger.exception("Internal server error")
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))


