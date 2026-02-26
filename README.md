# Dataloop UI Application Examples

Example applications demonstrating how to build and deploy UI apps on the [Dataloop](https://dataloop.ai) platform. Each example showcases a different application slot type.

## Examples

| Example | Slot Type | Description |
|---|---|---|
| [Panel + Toolbar](./example-panel-toolbar/) | `dialog` + toolbar | A popup panel triggered by a toolbar button in the dataset browser |
| [Route Slot](./example-route-slot/) | `route` | A full-page application accessible from the platform sidebar |

## Architecture

Both examples share the same local development architecture:

```
Browser (https://localhost:3004)
  └─► Nginx (SSL reverse proxy, port 3000)
        ├─► Vite dev server (port 8084) — serves Vue 3 frontend with hot-reload
        └─► FastAPI (port 5463) — Python backend using the Dataloop SDK
```

The Docker container bundles all three services. Your project directory is volume-mounted at `/tmp/app` so code changes are reflected immediately.

## Prerequisites

- **Docker** — for running the containerized dev environment
- **Python 3.10+** — for running `install.py` and the Dataloop SDK
- **Node.js 16+** — used inside the container for Vite; also needed if building frontend locally
- **Dataloop account** — sign up at [console.dataloop.ai](https://console.dataloop.ai)

## Quick Start

Each example is a self-contained project. Navigate into any example directory and follow its README:

```bash
cd example-panel-toolbar   # or example-route-slot
```

### 1. Set up credentials

```bash
cp env.example .env
# Edit .env with your Dataloop token (see the example README for details)
```

### 2. Build and run locally (Docker)

```bash
docker build --rm -f local.Dockerfile -t my-app:latest .
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" my-app:latest
```

### 3. Open the app

```
https://localhost:3004/model_configurator   # panel-toolbar example
https://localhost:3004/route-slot           # route-slot example
```

> **Note:** Uses HTTPS with a self-signed certificate. Accept the browser warning to proceed.

### 4. Deploy to the platform

```bash
python scripts/install.py -project_id YOUR_PROJECT_ID
```

## Slot Types Overview

| Slot Type | Trigger | Display | Best For |
|---|---|---|---|
| `dialog` + toolbar | Toolbar button click | Popup dialog (configurable size) | Quick actions, configuration panels |
| `route` | Sidebar navigation icon | Full page | Dashboards, full applications |

## Documentation

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)
- [Dataloop SDK Documentation](https://developers.dataloop.ai)
