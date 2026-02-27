# Walkthrough: example-route-slot

Live testing performed 2026-02-26 against both `main` (broken) and `improve/readme-and-dx` (fixed).

---

## Before (on `main`)

### Step 1 — cp env.example .env

```
$ cp env.example .env
cp: cannot stat 'env.example': No such file or directory
```

**FAILURE: Immediate blocker at Step 2 of the README. File doesn't exist.**

### Step 2 — Missing login.py

```
$ ls scripts/login.py
ls: cannot access 'scripts/login.py': No such file or directory
```
README project structure diagram lists `login.py` — it doesn't exist.

**FAILURE: README lies about project structure.**

### Step 3 — start_dev.sh has no auth

```bash
#!/bin/sh
python -m uvicorn "scripts.app:app" ...
```
No call to `login.py`. The Dataloop SDK starts without authentication.

**FAILURE: Container runs but SDK is unauthenticated.**

### Step 4 — install.py uses interactive login

```python
dl.login()  # opens a browser popup
```
Panel-toolbar uses token auth from `.env`; route-slot uses interactive browser login. Inconsistent and won't work in CI/headless.

**FAILURE: install.py can't run non-interactively.**

### Step 5 — HTTP vs HTTPS

Same as panel-toolbar. README says `http://`, nginx requires `https://`.
```
$ curl http://localhost:3004/route-slot   → 400 Bad Request
$ curl https://localhost:3004/route-slot  → 200 OK
```

Following the README's HTTP URL:

![Route-slot HTTP — 400 Bad Request](./walkthrough-screenshots/phase1_route_http.png)

Using HTTPS instead (undocumented):

![Route-slot HTTPS — app loads](./walkthrough-screenshots/phase1_route_https.png)

> Note: The route-slot app renders blank in a standalone browser because the Vue components need the Dataloop platform frame driver context to display content. The 200 response and correct HTML confirm the server is working.

**FAILURE: README URL doesn't work.**

### Before — Difficulty Rating: 4/10 — impossible to complete

A new developer following the README literally would be blocked within the first 2-3 steps. The `env.example` file is missing and `login.py` doesn't exist.

---

## After (on `improve/readme-and-dx`)

### Step 1 — env.example exists

```
$ cat env.example   # identical template
```

PASS

### Step 2 — login.py exists

```
$ cat scripts/login.py
import dtlpy as dl
from dotenv import load_dotenv
...
dl.login_token(token)
```

PASS

### Step 3 — start_dev.sh calls login.py

```bash
#!/bin/sh
# Authenticate to Dataloop using dtlpy with env and token from .env
python scripts/login.py
python -m uvicorn ...
```

PASS

### Step 4 — Container starts cleanly

```
INFO:     Uvicorn running on http://0.0.0.0:5463
VITE v5.4.21  ready in 2907 ms
  ➜  Local:   http://localhost:8084/route-slot
```

PASS

### Step 5 — HTTPS URL works

```
$ curl -sk https://localhost:3004/route-slot → 200
  <!DOCTYPE html>
  <html lang="en">
    <title>Route Slot Example</title>
    ...
```

![Route-slot HTTPS after fix — app loads](./walkthrough-screenshots/phase3_route_https.png)

> Note: Renders blank in standalone browser (needs Dataloop platform context). The 200 response and correct HTML confirm the server is working correctly.

PASS

### Step 6 — HTTP returns 400 (expected — documented in troubleshooting)

![Route-slot HTTP after fix — 400 is expected, README now says HTTPS](./walkthrough-screenshots/phase3_route_http.png)

PASS — the README now correctly documents `https://` and the troubleshooting table explains this.

### Step 7 — install.py uses token auth

```python
dl.setenv(env)
dl.login_token(token)
```
Matches panel-toolbar. No browser popup.

PASS

### After — Difficulty Rating: 9/10 — straightforward, works first try

---

## Changes That Fixed It

| File | What Changed |
|------|-------------|
| `example-route-slot/scripts/login.py` | **Created** — was missing entirely |
| `example-route-slot/env.example` | **Created** — template so users know what to put in `.env` |
| `example-route-slot/start_dev.sh` | **Added** `python scripts/login.py` before uvicorn |
| `example-route-slot/scripts/install.py` | **Replaced** interactive `dl.login()` with token auth from `.env` |
| `example-route-slot/README.md` | **Rewritten** — accurate project structure, standardized auth |
| `README.md` (root) | **Updated** — architecture diagram, credential setup, HTTPS URLs |
