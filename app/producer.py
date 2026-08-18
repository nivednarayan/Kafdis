from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def emit_event(client_id, allowed, limit, window_seconds):
    event = {
        "client_id": client_id,
        "allowed": allowed,
        "limit": limit,
        "window_seconds": window_seconds,
        "timestamp": int(time.time() * 1000)
    }
    producer.send('rate-limit-events', event)
    producer.flush()
