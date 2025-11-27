import requests
import time
import argparse
import random
import json

SAMPLES = [
    "I love this product! It works amazingly well.",
    "This is the worst experience I've had.",
    "Not bad, could be better.",
    "I would recommend this to my friends.",
    "Terrible. Will not buy again.",
]

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://ml-api-svc/predict')
parser.add_argument('--rate', type=float, default=1.0, help='requests per second')
parser.add_argument('--duration', type=int, default=60)
args = parser.parse_args()

end = time.time() + args.duration
results = []
while time.time() < end:
    t0 = time.time()
    text = random.choice(SAMPLES)
    try:
        r = requests.post(args.url, json={'text': text}, timeout=5)
        data = r.json()
        results.append({'status': r.status_code, 'resp': data, 'time': time.time()})
    except Exception as e:
        results.append({'status': 'err', 'error': str(e), 'time': time.time()})
    sleep_for = max(0, 1.0/args.rate - (time.time() - t0))
    time.sleep(sleep_for)

# Dump results
print(json.dumps(results, indent=2))
