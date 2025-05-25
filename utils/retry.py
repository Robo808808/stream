import time

def retry_with_backoff(fn, retries=3, base_delay=2, *args, **kwargs):
    for i in range(retries):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            delay = base_delay * (2 ** i)
            print(f"🔁 Retry {i+1}/{retries} failed: {e}, retrying in {delay}s...")
            time.sleep(delay)
    raise Exception(f"❌ All {retries} retries failed for {fn.__name__}")
