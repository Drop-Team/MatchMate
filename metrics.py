from prometheus_client import Counter, Gauge

alias_errors = Counter('alias_errors', 'Alias errors')
timeout_errors = Counter('timeout_errors', 'Timeout errors')

users = Gauge('users', 'Users number')

storage_records = Gauge('storage_records', 'Storage records number')

match_attempt = Counter('match_attempt', 'Match attempt')
unmatch_attempt = Counter('unmatch_attempt', 'Unmatch attempt')

successful_matches = Counter('successful_matches', 'Successful matches')
