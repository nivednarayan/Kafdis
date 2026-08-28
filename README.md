# Kafdis — Distributed Rate Limiter as a Service

## What it is
Kafdis is a production-grade distributed rate limiter that prevents resource exhaustion attacks by enforcing per-client request limits. 
Any service can call it to check whether a request should be allowed or rejected.

## Architecture
```
Client
|
Nginx (port 8080) — load balancer
|
├── app instance 1
├── app instance 2
└── app instance 3
|
├── Redis — sliding window counter (sorted sets)
├── Kafka — audit log (rate-limit-events topic)
└── Prometheus — metrics scraping (/metrics/)
|
Grafana — real time dashboard
```


## How it works
Each client gets a Redis sorted set keyed by their ID. Every request is stored as a UUID with a millisecond timestamp as the score. On every check, a Lua script runs atomically — removes entries outside the current window, counts remaining entries, rejects if over limit, adds the request if allowed. The Lua script ensures atomicity across all distributed instances — no race conditions.

## Tech Stack
- **Redis** — in-memory sorted sets for the sliding window counter
- **FastAPI** — async API layer, POST /check returns 200 or 429
- **Kafka** — audit log, every allow/reject decision emitted to `rate-limit-events`
- **Nginx** — reverse proxy and load balancer across 3 app instances
- **Prometheus + Grafana** — real time monitoring dashboard

## How to Run
```bash
docker compose up --build -d --scale app=3
```
- API: http://localhost:8080/check
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

## API
```bash
curl -X POST http://localhost:8080/check \
  -H "Content-Type: application/json" \
  -d '{"client_id": "user:123", "limit": 100, "window_seconds": 60}'
```

## Benchmark — k6 load test, 50 VUs, 30s
| Metric | Value |
|---|---|
| Throughput | 1,239 req/s |
| Avg latency | 40ms |
| p95 latency | 103ms |
| Error rate | 0% |

## Dashboard

