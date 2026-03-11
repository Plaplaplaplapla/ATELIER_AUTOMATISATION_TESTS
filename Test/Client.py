import time
import requests

DEFAULT_TIMEOUT = 3
MAX_RETRY = 1


def request_json(url: str, timeout: int = DEFAULT_TIMEOUT, max_retry: int = MAX_RETRY):
    attempt = 0
    last_error = None

    while attempt <= max_retry:
        start = time.perf_counter()

        try:
            response = requests.get(url, timeout=timeout)
            latency_ms = (time.perf_counter() - start) * 1000

            if response.status_code == 429 and attempt < max_retry:
                retry_after = response.headers.get("Retry-After")
                wait_s = float(retry_after) if retry_after else 1.0
                time.sleep(wait_s)
                attempt += 1
                continue

            if 500 <= response.status_code <= 599 and attempt < max_retry:
                time.sleep(1)
                attempt += 1
                continue

            return {
                "ok": True,
                "status_code": response.status_code,
                "content_type": response.headers.get("Content-Type", ""),
                "json": response.json() if "application/json" in response.headers.get("Content-Type", "") else None,
                "latency_ms": latency_ms,
                "error": None,
            }

        except requests.Timeout as exc:
            last_error = f"timeout: {exc}"
            if attempt < max_retry:
                time.sleep(1)
                attempt += 1
                continue
            return {
                "ok": False,
                "status_code": None,
                "content_type": "",
                "json": None,
                "latency_ms": None,
                "error": last_error,
            }

        except requests.RequestException as exc:
            last_error = str(exc)
            return {
                "ok": False,
                "status_code": None,
                "content_type": "",
                "json": None,
                "latency_ms": None,
                "error": last_error,
            }
