from flask import Blueprint
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

metrics_bp = Blueprint('metrics', __name__)

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests', [
        'method',
        'endpoint'
    ]
)


@metrics_bp.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
