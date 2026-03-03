# Example: Route Slot Application

This example builds a full-page application that appears as an icon in the Dataloop platform's left sidebar. Clicking the icon navigates to your app's dedicated page.

Use this pattern when you want to build a standalone tool, dashboard, or multi-view application inside the platform.

[What You Get](#what-youll-end-up-with) | **[Quick Start](#quick-start)** | [Local Development](#local-development) | [Project Structure](#project-structure) | [How It Works](#how-the-route-slot-pattern-works) | [Customization](#customization-guide) | [Troubleshooting](#troubleshooting)

## What You'll End Up With

- A **sidebar icon** (pencil/edit icon) in the Dataloop platform's left navigation
- Clicking it opens your app as a **full page** within the platform
- The example page displays the current user, project, and theme, with an interactive button
- A Python backend with a health-check endpoint (ready for you to add your own API)

When deployed, your app's icon appears in the sidebar alongside Dataloop's built-in pages like Datasets, Pipelines, and Tasks.

## Quick Start

Deploy this app to your Dataloop project in two steps:

```bash
pip install dtlpy
python scripts/install.py --project_id YOUR_PROJECT_ID
```

The script opens a browser window to log in if needed. Once it finishes, open your project in the Dataloop console and look for the new icon in the left sidebar.

Want to customize the app first? Continue to [Local Development](#local-development) below.

## Local Development

To run and customize the app locally before deploying, you'll need:

1. **Docker Desktop** installed and running ([download](https://www.docker.com/products/docker-desktop/))
2. **Python 3.10 or newer** ([download](https://www.python.org/downloads/))
3. **A Dataloop account** with at least one project — sign up at [console.dataloop.ai](https://console.dataloop.ai)

## Step-by-Step Setup

### Step 1: Build the Docker image

```bash
docker build --rm -f local.Dockerfile -t example-route-slot:latest .
```

This takes a few minutes the first time. It downloads a base image, installs Python and Node.js dependencies, and generates an SSL certificate.

### Step 2: Start the container

**macOS / Linux / Git Bash:**

```bash
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" example-route-slot:latest
```

**Windows Command Prompt:**

```cmd
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" example-route-slot:latest
```

**Windows PowerShell:**

```powershell
docker run -p 3004:3000 -it -v "${PWD}:/tmp/app" example-route-slot:latest
```

Wait for the startup to finish. You'll see output from several services. The app is ready when you see:

```
VITE v5.x.x  ready in xxxxms
```

### Step 3: Open the app

Go to this URL in your browser:

```
https://localhost:3004/route-slot
```

**Important:** The URL starts with `https`, not `http`. Your browser will show a certificate warning because the app uses a self-signed certificate for local development. This is normal.

- **Chrome**: Click "Advanced" then "Proceed to localhost (unsafe)"
- **Firefox**: Click "Advanced" then "Accept the Risk and Continue"
- **Edge**: Click "Advanced" then "Continue to localhost (unsafe)"

> **Note:** When running locally (outside the Dataloop platform), the page may appear blank or show minimal content. This is expected — the app's Vue components use the platform's frame driver to get user and project data, which is only available when running inside the platform. A successful `200 OK` response and the correct HTML title confirm the server is working.

## Making Changes

Your project folder is mounted into the container. While the container is running:

- **Frontend changes** (`src/` folder): Edits appear in the browser automatically via Vite HMR — no restart needed.
- **Backend changes** (`scripts/app.py`): Also hot-reloaded automatically — uvicorn runs with `--reload` in dev mode.
- **Structural changes** (new dependencies in `package.json`, changes to `scripts/main.py`, Dockerfile changes): Stop the container (`Ctrl+C`), rebuild the image (Step 1), and restart (Step 2).

## Project Structure

```
example-route-slot/
├── src/                    # Frontend source code (Vue.js)
│   ├── main.ts             # App entry point
│   ├── App.vue             # Main UI component
│   └── style.css           # Styles
├── scripts/                # Backend code (Python)
│   ├── app.py              # API server — health endpoint (add your own here)
│   ├── install.py          # Publishes and installs the app to Dataloop
│   └── main.py             # Entry point used by the platform in production
├── panels/route-slot/      # Pre-built frontend (used in production)
├── requirements.txt        # Python dependencies for the deployed service
├── dataloop.json           # App manifest — defines the panel, route, and service
├── local.Dockerfile        # Docker image for local development
├── nginx.conf              # Routes HTTPS traffic to frontend and backend
├── start_dev.sh            # Startup script that runs inside the container
├── package.json            # Node.js dependencies
└── vite.config.ts          # Frontend build configuration
```

## How the Route Slot Pattern Works

In Dataloop, applications are defined by a `dataloop.json` manifest. This example declares a **panel** with a `route` slot type, which tells the platform: "I have a UI that should live at its own URL path and appear as a sidebar icon."

The key configuration:

- **`type: "route"`** — makes this a full-page app (not a popup)
- **`path: "route-slot"`** — the URL path within the platform
- **`sidePanelConfig.icon`** — the icon shown in the sidebar
- **`sidePanelConfig.orderId`** — where in the sidebar the icon appears
- **`requiredResources: ["project"]`** — the icon only shows when inside a project

Inside your app, the **frame driver** (`window.dl`) connects your Vue.js frontend to the platform, giving you access to the current project, user, theme, and platform events.

### When to use Route Slot vs Panel + Toolbar

| | Route Slot (this example) | Panel + Toolbar |
|---|---|---|
| **Appears as** | Full page via sidebar icon | Popup dialog via toolbar button |
| **Best for** | Dashboards, multi-view tools, standalone apps | Quick actions, settings forms, config dialogs |
| **Page scope** | Has its own dedicated page | Opens over an existing page |

## Customization Guide

### Changing the Frontend

Edit `src/App.vue` — this is the main UI component. Vite HMR picks up changes automatically.

Key areas:
- **Template** (top of file): HTML structure using `@dataloop-ai/components` (DlButton, DlThemeProvider, etc.)
- **Script** (middle): Vue 3 Composition API logic — reactive state, event handlers
- **Platform integration**: `window.dl` gives you access to the current project, user, theme, and events via `@dataloop-ai/jssdk`

### Changing the Backend API

Add routes in `scripts/app.py`. The existing health endpoint shows the pattern. Nginx already forwards all `/api/*` requests to the Python backend, so new routes are available immediately.

### Changing the Manifest

`dataloop.json` controls how your app appears in the platform:

- **`components.panels[0].supportedSlots[0].configuration.route.path`** — the URL path for your page
- **`components.panels[0].supportedSlots[0].configuration.route.sidePanelConfig.icon`** — the sidebar icon (e.g. `icon-dl-edit`)
- **`components.panels[0].supportedSlots[0].configuration.route.sidePanelConfig.orderId`** — position in the sidebar (lower = higher up)
- **`components.services[0].runtime`** — production resource allocation (pod type, replicas)

### Adding Dependencies

- **Frontend (npm)**: Add to `package.json`, then restart the container (the startup script runs `npm install`)
- **Backend (pip)**: Add to both `Dockerfile` and `local.Dockerfile`, then rebuild the image (`docker build`)

### Rebuilding the Production Frontend

```bash
npm run build
```

This outputs compiled files to `panels/route-slot/`. These files are included in the DPK when you run `install.py`.

## Troubleshooting

| What you see | What to do |
|---|---|
| Browser shows "400 Bad Request" | You used `http://` instead of `https://`. Change the URL to start with `https://`. |
| Browser shows a certificate warning | This is expected. Click through the warning (see Step 3). |
| Spinner stays forever in the browser | If loading lasts more than ~2 seconds locally, something is wrong. The app should render and show `N/A` for platform fields outside Dataloop context. |
| User/Project show `N/A` locally | This is expected outside Dataloop context. Install the app in the Dataloop platform to see real values. |
| `docker build` fails downloading the base image | The base image is hosted on `hub.dataloop.ai` which may require authentication. Try removing `--pull` from the build command if present. |
| Port 3004 is already in use | Another container or process is using that port. Run `docker ps` to find it, then `docker stop <container_id>`. |

## Learn More

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)
- [Single Page Application Tutorial](https://developers.dataloop.ai/tutorials/applications/single_page_application/chapter)
- [Dataloop Applications Overview](https://developers.dataloop.ai/tutorials/applications/introduction/chapter)
- [Dataloop SDK Documentation](https://developers.dataloop.ai)
