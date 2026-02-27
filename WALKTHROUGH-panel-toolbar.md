# Walkthrough: example-panel-toolbar

Live testing performed 2026-02-26 against both `main` (broken) and `improve/readme-and-dx` (fixed).

---

## Before (on `main`)

### Step 1 — README auth instructions

README says:
```bash
pip install dtlpy
dl.login()
```
But `scripts/login.py` actually reads `DTLPY_ENV` and `DTLPY_TOKEN` from `.env` and calls `dl.login_token()`. A user following the README would never create a `.env` file.

**FAILURE: Auth instructions don't match how the code works.**

### Step 2 — Missing env.example

```
$ ls env.example
ls: cannot access 'env.example': No such file or directory

$ ls .env
ls: cannot access '.env': No such file or directory
```

**FAILURE: No template file. User has no idea what env vars are needed.**

### Step 3 — Container without .env

```
$ docker run ... examplepaneltoolbar:phase1
Traceback (most recent call last):
  File "/tmp/app/scripts/login.py", line 9, in <module>
    dl.setenv(env)
  File ".../api_client.py", line 1516, in setenv
    if env.startswith('http'):
AttributeError: 'NoneType' object has no attribute 'startswith'
```

**FAILURE: login.py crashes — DTLPY_ENV is None because no .env exists.**

### Step 4 — HTTP vs HTTPS

```
$ curl http://localhost:3004/model_configurator   → 400 Bad Request
$ curl https://localhost:3004/model_configurator  → 200 OK
```
README says `http://localhost:3004/model_configurator`. Nginx only listens on SSL (`listen 3000 ssl;`).

Following the README's HTTP URL:

![Panel-toolbar HTTP — 400 Bad Request](./walkthrough-screenshots/phase1_panel_http.png)

Using HTTPS instead (undocumented):

![Panel-toolbar HTTPS — app loads](./walkthrough-screenshots/phase1_panel_https.png)

**FAILURE: README URL doesn't work. Users get a 400 error page with no explanation.**

### Before — Difficulty Rating: 4/10 — impossible to complete

A new developer following the README literally would be blocked within the first 2-3 steps. The app crashes on start because no `.env` template exists.

---

## After (on `improve/readme-and-dx`)

### Step 1 — env.example exists

```
$ cat env.example
# Dataloop environment (usually "prod")
DTLPY_ENV=prod
# Your Dataloop authentication token
...
DTLPY_TOKEN=your_token_here
```

PASS

### Step 2 — cp env.example .env

```
$ cp env.example .env
$ # Edit .env with real token
```

PASS

### Step 3 — Docker build

```
$ docker build --rm -f local.Dockerfile -t examplepaneltoolbar:phase3 .
# ... builds successfully
```

PASS (note: `--pull` removed from README default, avoiding potential auth issues with `hub.dataloop.ai`)

### Step 4 — Container starts cleanly

```
INFO:     Uvicorn running on http://0.0.0.0:5463
VITE v5.1.6  ready in 4065 ms
  ➜  Local:   http://localhost:8084/model_configurator
```
No login.py errors. All three services (uvicorn, Vite, nginx) started.

PASS

### Step 5 — HTTPS URL works

```
$ curl -sk https://localhost:3004/model_configurator → 200
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>DL Model Configurator - 2025</title>
    ...
```

![Panel-toolbar HTTPS after fix — Model Training Configuration UI](./walkthrough-screenshots/phase3_panel_https.png)

PASS

### Step 6 — HTTP still returns 400 (expected — documented in troubleshooting)

![Panel-toolbar HTTP after fix — 400 is expected, README now says HTTPS](./walkthrough-screenshots/phase3_panel_http.png)

PASS — the README now correctly documents `https://` and the troubleshooting table explains this.

### Step 7 — API responds

```
$ curl -sk https://localhost:3004/api/models → 422
```
422 is expected (needs query params from the Vue frontend). Backend is alive and authenticated.

PASS

### After — Difficulty Rating: 9/10 — straightforward, works first try

---

## Changes That Fixed It

| File | What Changed |
|------|-------------|
| `example-panel-toolbar/env.example` | **Created** — template so users know what to put in `.env` |
| `example-panel-toolbar/README.md` | **Rewritten** — HTTPS URLs, env setup steps, troubleshooting |
| `README.md` (root) | **Updated** — architecture diagram, credential setup, HTTPS URLs |
