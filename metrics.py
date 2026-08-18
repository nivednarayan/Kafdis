from prometheus_client import Counter

allowed_count = Counter('allowed_request_counter', 'No: of incoming requests allowed', ["client_id"])
rejected_count = Counter('rejected_request_counter', 'No: of incoming requests rejected', ["client_id"])         
