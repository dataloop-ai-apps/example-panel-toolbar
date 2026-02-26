# Example Panel + Toolbar - Model Configurator

A demo application for configuring machine learning models in the Dataloop platform. This UI panel allows users to select models, modify their configurations, and create new models by cloning existing ones.

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
│   └── install.py         # Publish and install to Dataloop
├── panels/                # Built frontend output
│   └── model_configurator/
├── dataloop.json          # Dataloop app manifest (production)
├── dataloop_dev.json      # Dataloop app manifest (development)
├── package.json           # Node.js dependencies
├── vite.config.ts         # Vite build configuration
├── Dockerfile             # Production Docker image
├── local.Dockerfile       # Local development Docker image
├── nginx.conf             # Nginx reverse proxy config
└── start_dev.sh           # Development startup script
```

## Features

- **Model Selection**: Browse and select from available models in your project
- **Configuration Editor**: Edit model parameters with different input types (text, number, checkbox, JSON)
- **Model Cloning**: Create new models by cloning existing ones with modified configurations
- **Configuration Updates**: Save changes to existing model configurations

## Local Development Setup

### Prerequisites

- Python 3.8+
- Docker
- Node.js 16+
- Dataloop account and project

### Step 1: Dataloop Authentication

```bash
pip install dtlpy
dl.login()
```

### Step 2: Docker Build and Run

**Build:**

```bash
docker build --pull --rm -f 'local.Dockerfile' -t 'examplepaneltoolbar:latest' '.'
```

**Windows:**

```cmd
docker build --pull --rm -f local.Dockerfile -t examplepaneltoolbar:latest .
```

**Run:**

```bash
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" examplepaneltoolbar:latest
```

**Windows:**

```cmd
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" examplepaneltoolbar:latest
```

### Step 3: Access the Application

```
http://localhost:3004/model_configurator
```

For more details on local development, see [Building Web Apps](https://developers.dataloop.ai/tutorials/applications/web_application/chapter).

## Platform Deployment

```bash
python scripts/install.py -project_id YOUR_PROJECT_ID
```
