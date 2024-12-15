import logging
from fastapi import FastAPI, status
import time
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.error_handler import setup_error_handlers
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge, Counter, generate_latest
from api.compare import routes as compare_router
from env import env

uptime_gauge = Gauge(
    "app_uptime_seconds", "Uptime of the FastAPI application in seconds"
)

# Route-specific counters
route_counter = Counter("route_hits_total", "Total number of hits per route", ["route"])

# Create FastAPI app
app = FastAPI()


# Uptime tracking
start_time = time.time()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow selecte origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Add exception handlers
setup_error_handlers(app)

# Include all the routes
app.include_router(compare_router.router)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define counters for each category of HTTP status code
counter_2xx = Counter(
    "http_2xx_requests_total", "Total 2xx requests", ["path", "method"]
)
counter_3xx = Counter(
    "http_3xx_requests_total", "Total 3xx requests", ["path", "method"]
)
counter_4xx = Counter(
    "http_4xx_requests_total", "Total 4xx requests", ["path", "method"]
)
counter_5xx = Counter(
    "http_5xx_requests_total", "Total 5xx requests", ["path", "method"]
)


# Middleware to track response codes
@app.middleware("http")
async def track_status_codes_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return PlainTextResponse("Internal server error", status_code=500)

    # Increment counters based on the response status code
    if 200 <= response.status_code < 300:
        counter_2xx.labels(path=request.url.path, method=request.method).inc()
    elif 300 <= response.status_code < 400:
        counter_3xx.labels(path=request.url.path, method=request.method).inc()
    elif 400 <= response.status_code < 500:
        counter_4xx.labels(path=request.url.path, method=request.method).inc()
    elif 500 <= response.status_code < 600:
        counter_5xx.labels(path=request.url.path, method=request.method).inc()

    return response


# Set up Prometheus Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


# ============= Sample route =============
@app.get("/")
def home() -> dict[str, str]:
    """Root endpoint that returns a welcome message."""

    return {"message": "Success, Welcome to API"}


# ============= Metrics Route =================
@app.get("/metrics", tags=["API Stats"])
def metrics():
    # Update uptime gauge
    current_uptime = time.time() - start_time
    uptime_gauge.set(current_uptime)
    logging.info("Uptime updated: %s seconds", current_uptime)
    return PlainTextResponse(content=generate_latest(), media_type="text/markdown")
