from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import logging
import time

app = FastAPI(title="Kubernetes Observability Demo")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of application requests"
)


@app.get("/")
def root():
    REQUEST_COUNT.inc()
    logging.info("Root endpoint requested")
    return {
        "application": "kubernetes-observability-demo",
        "status": "running"
    }


@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status": "healthy"}


@app.get("/slow")
def slow():
    REQUEST_COUNT.inc()
    logging.warning("Slow endpoint requested")
    time.sleep(5)
    return {"status": "completed", "delay": "5 seconds"}


@app.get("/error")
def error():
    REQUEST_COUNT.inc()
    logging.error("Simulated application failure")
    return Response(
        content='{"error":"simulated failure"}',
        status_code=500,
        media_type="application/json"
    )


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
