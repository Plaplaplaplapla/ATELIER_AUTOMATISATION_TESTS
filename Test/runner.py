from statistics import mean
from tester.client import request_json

BASE_URL = "https://pokeapi.co/api/v2"


def percentile_95(values):
    if not values:
        return None
    values = sorted(values)
    index = int(0.95 * (len(values) - 1))
    return values[index]


def run_qos(n: int = 10):
    latencies = []
    errors = 0
    results = []

    for _ in range(n):
        result = request_json(f"{BASE_URL}/pokemon/pikachu")
        results.append(result)

        if result["status_code"] is None or (result["status_code"] >= 400):
            errors += 1

        if result["latency_ms"] is not None:
            latencies.append(result["latency_ms"])

    avg_latency = mean(latencies) if latencies else None
    p95_latency = percentile_95(latencies)
    error_rate = errors / n if n else 0
    availability = (n - errors) / n if n else 0

    return {
        "runs": n,
        "avg_latency_ms": avg_latency,
        "p95_latency_ms": p95_latency,
        "error_rate": error_rate,
        "availability": availability,
        "results": results,
    }


if __name__ == "__main__":
    print(run_qos(10))
