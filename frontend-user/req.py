import requests


def get(url, *args, timeout, **kargs):
    resp = requests.get(url, *args, timeout=timeout, **kargs)
    if resp.status_code != 200:
        raise RuntimeError({"message": f"Got status code {resp.status_code}"})

    payload = resp.json()
    msg = payload.get("message", None)
    if msg is not None:
        raise RuntimeError(str(msg))

    return payload["data"]
