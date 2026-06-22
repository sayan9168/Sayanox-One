RULES = [
    {"name": "large response", "fn": lambda resp: len(resp.content) > 10_000_000},
    {"name": "stack trace leak", "fn": lambda resp: "Traceback" in resp.text}
]
