from flask import Flask, jsonify
import redis
import time
import requests
import os

app = Flask(__name__)
start_time = time.time()
SERVICE_URLS = [
   {"name":"google", "url": "https://www.google.com"},
   {"name":"github", "url": "https://www.github.com"}, 
   {"name":"stackoverflow", "url": "https://www.stackoverflow.com"}
]

r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)


@app.route('/health')
def health():
    uptime = int(time.time() - start_time)
    return jsonify({
        'status': 'healthy',
        'uptime_seconds': f"{uptime}s"
    })

@app.route('/services')
def services():
    results = []
    for service in SERVICE_URLS:
        try:
            
            start = time.time()
            response = requests.get(service['url'], timeout=5)
            r.incr('total_requests')
            r.incr('services_checked')
            latency = int((time.time() - start) * 1000)
            results.append({
                'name': service['name'],
                'status': 'up' if response.status_code == 200 else 'down',
                'latency_ms': latency
            })
        except Exception:
            results.append({
                'name': service['name'],
                'status': 'down',
                'latency_ms': None
            })

    return jsonify({"services": results})

@app.route('/metrics')
def metrics():
    r.incr('total_requests')
    return jsonify({
        "total_requests": int(r.get('total_requests') or 0),
        "services_checked": int(r.get('services_checked') or 0)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
