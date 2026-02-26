# Example Route Slot Application

A simple Dataloop platform application demonstrating a **route slot** panel. Route slots appear as dedicated pages in the Dataloop platform sidebar, accessible via a navigation icon.

## What is a Route Slot?

Unlike dialog/panel slots (which open as popups triggered by toolbars), a **route slot** registers a full-page route in the Dataloop platform. It appears as an icon in the left sidebar and navigates to a dedicated page within the platform.

Key configuration in `dataloop.json`:

```json
"supportedSlots": [
    {
        "type": "route",
        "configuration": {
            "route": {
                "name": "Route Slot Example",
                "path": "route-slot",
                "src": "route-slot/index.html",
                "sidePanelConfig": {
                    "icon": "icon-dl-edit",
                    "orderId": 7,
                    "requiredResources": ["project"]
                }
            }
        }
    }
]
```

## Project Structure

```
example-route-slot/
├── src/                    # Vue.js frontend
│   ├── main.ts            # Entry point - initializes Dataloop frame driver
│   ├── App.vue            # Main component - displays user/project info
│   └── style.css          # Global styles
├── scripts/               # Python backend
│   ├── main.py            # Dataloop service runner (starts uvicorn)
│   ├── app.py             # FastAPI server (serves static files)
│   ├── install.py         # Publish and install to Dataloop
│   └── login.py           # Authentication helper
├── panels/                # Built frontend output
│   └── route-slot/
├── dataloop.json          # Dataloop app manifest
├── package.json           # Node.js dependencies
├── vite.config.ts         # Vite build configuration
├── Dockerfile             # Production Docker image
├── local.Dockerfile       # Local development Docker image
├── nginx.conf             # Nginx reverse proxy config
├── start_dev.sh           # Development startup script
└── env.example            # Environment variables template
```

## Local Development Setup

### Prerequisites

- Python 3.8+
- Docker
- Node.js 16+
- Dataloop account and project

### Step 1: Dataloop Authentication

```bash
pip install dtlpy
python3
```

```python
import dtlpy as dl
dl.setenv('prod')
dl.login()
token = dl.token()
print(f"Your token: {token}")
```

### Step 2: Environment Setup

```bash
cp env.example .env
# Edit .env with your actual token
```

### Step 3: Docker Build and Run

**Build:**

```bash
docker build --pull --rm -f 'local.Dockerfile' -t 'example-route-slot:latest' '.'
```

**Run:**

```bash
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" example-route-slot:latest
```

**Windows:**

```cmd
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" example-route-slot:latest
```

### Step 4: Access the Application

```
http://localhost:3004/route-slot
```

## Platform Deployment

```bash
# Create .env with your credentials, then:
python scripts/install.py -project_id YOUR_PROJECT_ID
```

## Comparison with Panel+Toolbar Example

| Feature | Panel+Toolbar | Route Slot |
|---|---|---|
| **Slot type** | `dialog` | `route` |
| **Trigger** | Toolbar button click | Sidebar navigation icon |
| **Display** | Popup dialog (configurable size) | Full page |
| **Use case** | Quick actions, configuration | Full applications, dashboards |
