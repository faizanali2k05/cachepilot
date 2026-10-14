# cachepilot

Keep freshness policy separate from Redis, disk, HTTP, or in-memory storage.

```bash
python -m pip install cachepilot
```

```python
from cachepilot import CachePolicy, is_usable

policy = CachePolicy(fresh_for=30, stale_for=120)
decision = policy.decide(age=75, error=True)
if is_usable(decision):
    return cached_value
```

`FRESH`, `STALE`, `STALE_IF_ERROR`, and `MISS` are transport-neutral decisions. Negative ages and invalid windows are rejected so clock and policy mistakes do not silently serve data.
