# Example Panel + Toolbar - Model Configurator

A demo application for configuring machine learning models in the Dataloop platform. This UI panel allows users to select models, modify their configurations, and create new models by cloning existing ones.

## How It Works

This app runs inside a Docker container with three components:

- **Nginx** — SSL reverse proxy on port 3000, routes `/api` to FastAPI and everything else to Vite
- **Vite** — Vue 3 dev server on port 8084, hot-reloads the frontend from `src/`
- **FastAPI** — Python backend on port 5463, handles model CRUD via the Dataloop SDK

The Docker container is accessed at `https://localhost:3004`, which maps to nginx on port 3000 inside the container.

## What is a Panel + Toolbar Slot?

A **panel** with a `dialog` slot type opens as a popup window within the Dataloop platform. It is triggered by a **toolbar** button placed in the dataset browser. This pattern is ideal for quick actions and configuration dialogs.

Key configuration in `dataloop.json`:

```json
"panels": [{
    "name": "model_configurator",
    "supportedSlots": [{
        "type": "dialog",
        "configuration": {
            "layout": { "width": 1000, "height": 800, "position": "center", "resizeable": true }
        }
    }]
}],
"toolbars": [{
    "name": "model_configurator_toolbar",
    "displayName": "Model Setup",
    "invoke": { "type": "panel", "namespace": "model_configurator" },
    "icon": "icon-dl-pipeline",
    "location": "datasetBrowserApps"
}]
```

## Project Structure

```
example-panel-toolbar/
├── src/                    # Vue.js frontend
│   ├── main.ts            # Entry point - initializes Dataloop frame driver
│   ├── App.vue            # Main component - model configuration UI
│   └── style.css          # Global styles
├── scripts/               # Python backend
│   ├── main.py            # Dataloop service runner (starts uvicorn)
│   ├── app.py             # FastAPI server (model CRUD + static files)
│   ├── login.py           # Authentication helper (reads .env)
│   └── install.py         # Publish and install to Dataloop
├── panels/                # Built frontend output (pre-built, committed)
│   └── model_configurator/
├── dataloop.json          # Dataloop app manifest (production)
├── dataloop_dev.json      # Dataloop app manifest (development)
├── package.json           # Node.js dependencies
├── vite.config.ts         # Vite build configuration
├── Dockerfile             # Production Docker image
├── local.Dockerfile       # Local development Docker image
├── nginx.conf             # Nginx reverse proxy config
├── start_dev.sh           # Development startup script
└── env.example            # Environment variables template
```

## Features

- **Model Selection**: Browse and select from available models in your project
- **Configuration Editor**: Edit model parameters with different input types (text, number, checkbox, JSON)
- **Model Cloning**: Create new models by cloning existing ones with modified configurations
- **Configuration Updates**: Save changes to existing model configurations

## Prerequisites

- Docker
- Python 3.10+
- Node.js 16+
- A [Dataloop](https://console.dataloop.ai) account with an existing project

## Local Development Setup

### Step 1: Get Your Dataloop Token

You need a Dataloop authentication token. Get one by running:

```bash
pip install dtlpy
python -c "import dtlpy as dl; dl.login(); print(dl.token())"
```

This opens a browser for login, then prints your token.

### Step 2: Create `.env`

```bash
cp env.example .env
```

Edit `.env` and replace `your_token_here` with the token from Step 1:

```
DTLPY_ENV=prod
DTLPY_TOKEN=<your actual token>
```

### Step 3: Build the Docker Image

```bash
docker build --rm -f local.Dockerfile -t examplepaneltoolbar:latest .
```

### Step 4: Run the Container

**macOS / Linux:**

```bash
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" examplepaneltoolbar:latest
```

**Windows (Command Prompt):**

```cmd
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" examplepaneltoolbar:latest
```

**Windows (PowerShell):**

```powershell
docker run -p 3004:3000 -it -v "${PWD}:/tmp/app" examplepaneltoolbar:latest
```

You should see output from login.py, uvicorn, npm install, and nginx starting up.

### Step 5: Access the Application

Open your browser to:

```
https://localhost:3004/model_configurator
```

> **Note:** The URL uses **HTTPS** (not HTTP). Your browser will show a certificate warning because the container uses a self-signed SSL certificate. Click "Advanced" > "Proceed" to continue.

## Platform Deployment

Deploy the app to your Dataloop project:

```bash
python scripts/install.py -project_id YOUR_PROJECT_ID
```

This requires a `.env` file with valid credentials (see Steps 1-2 above).

To find your project ID, go to your project in [Dataloop Console](https://console.dataloop.ai) and check the URL, or run:

```python
import dtlpy as dl
dl.login()
for p in dl.projects.list(): print(f"{p.name}: {p.id}")
```

## Frontend Development Notes

The `panels/model_configurator/` directory contains pre-built frontend assets that are committed to the repo. These are what get served in production.

During local development, Vite serves the frontend from `src/` with hot-reload. If you modify the frontend and want to update the production build:

```bash
npm install
npm run build
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `login.py` fails with token error | Check your `.env` file has a valid, non-expired `DTLPY_TOKEN` |
| `http://localhost:3004` doesn't load | Use `https://` — the server only speaks HTTPS |
| Browser shows certificate warning | Expected with self-signed cert — click through the warning |
| Container exits immediately | Make sure `.env` exists and has valid values |
| `--pull` fails on `docker build` | The base image `hub.dataloop.ai` may require auth. Remove `--pull` from the command |
| Port 3004 already in use | Stop other containers: `docker ps` then `docker stop <id>` |

## Documentation

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)
- [Dataloop SDK Documentation](https://developers.dataloop.ai)
