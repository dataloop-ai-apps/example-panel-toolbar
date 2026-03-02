# Example: Panel + Toolbar (Model Configurator)

This example builds a popup panel that appears when you click a toolbar button in the Dataloop dataset browser. The panel lets users browse, configure, and clone machine learning models in their project.

Use this pattern when you want to add a quick action or settings dialog to an existing Dataloop page.

## What You'll End Up With

- A **"Model Setup" button** in the dataset browser toolbar
- Clicking it opens a **popup dialog** (1000x800, centered, resizable)
- Inside the dialog: a form to select a model, edit its configuration, and save or clone it
- A Python backend that reads and writes model data through the Dataloop SDK

When deployed to the platform, it looks like this: a button appears in the dataset browser apps toolbar, and clicking it opens your panel as a dialog window.

## Before You Start

Make sure you have:

1. **Docker Desktop** installed and running ([download](https://www.docker.com/products/docker-desktop/))
2. **Python 3.10 or newer** ([download](https://www.python.org/downloads/))
3. **A Dataloop account** with at least one project — sign up at [console.dataloop.ai](https://console.dataloop.ai)

## Step-by-Step Setup

### Step 1: Get your Dataloop token

Open a terminal and run:

**macOS / Linux:**

```bash
pip3 install dtlpy
python3 -c "import dtlpy as dl; dl.login(); print(dl.token())"
```

**Windows (Command Prompt, PowerShell, or Git Bash):**

```bash
pip install dtlpy
python -c "import dtlpy as dl; dl.login(); print(dl.token())"
```

A browser window opens for you to log in. After login, your terminal prints a long token string. **Copy it** — you'll need it next.

> Tokens expire after 24 hours. If the app stops authenticating tomorrow, just repeat this step.

### Step 2: Create your `.env` file

From inside this directory (`example-panel-toolbar/`), copy the template:

**macOS / Linux / Git Bash:**

```bash
cp env.example .env
```

**Windows Command Prompt:**

```cmd
copy env.example .env
```

**Windows PowerShell:**

```powershell
Copy-Item env.example .env
```

Open `.env` in a text editor and fill in your values:

```
DTLPY_PROJECT_ID=your_project_id_here
DTLPY_ENV=prod
DTLPY_TOKEN=paste_your_token_here
```

The project ID is needed for deployment (`install.py`). To find it: open your project at [console.dataloop.ai](https://console.dataloop.ai) — the ID is the string after `/projects/` in the URL.

Save the file. Do not commit this file to git — it contains your personal credentials.

> **Private tenant?** If your organization uses a dedicated Dataloop environment instead of `console.dataloop.ai`, change `DTLPY_ENV` to your tenant name (e.g., `DTLPY_ENV=your-company`). Most users should leave it as `prod`.

### Step 3: Build the Docker image

```bash
docker build --rm -f local.Dockerfile -t examplepaneltoolbar:latest .
```

This takes a few minutes the first time. It downloads a base image, installs Python and Node.js dependencies, and generates an SSL certificate.

### Step 4: Start the container

**macOS / Linux / Git Bash:**

```bash
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" examplepaneltoolbar:latest
```

**Windows Command Prompt:**

```cmd
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" examplepaneltoolbar:latest
```

**Windows PowerShell:**

```powershell
docker run -p 3004:3000 -it -v "${PWD}:/tmp/app" examplepaneltoolbar:latest
```

Wait for the startup to finish. You'll see output from several services. The app is ready when you see:

```
VITE v5.x.x  ready in xxxxms
```

### Step 5: Open the app

Go to this URL in your browser:

```
https://localhost:3004/model_configurator
```

**Important:** The URL starts with `https`, not `http`. Your browser will show a certificate warning because the app uses a self-signed certificate for local development. This is normal.

- **Chrome**: Click "Advanced" then "Proceed to localhost (unsafe)"
- **Firefox**: Click "Advanced" then "Accept the Risk and Continue"
- **Edge**: Click "Advanced" then "Continue to localhost (unsafe)"

You should see the Model Training Configuration interface. If your project has models, you can select one from the dropdown to view and edit its configuration.

## Making Changes

Your project folder is mounted into the container. While the container is running:

- **Frontend changes** (`src/` folder): Edits appear in the browser automatically via Vite HMR — no restart needed.
- **Backend changes** (`scripts/app.py`): Also hot-reloaded automatically — uvicorn runs with `--reload` in dev mode.
- **Structural changes** (new dependencies in `package.json`, changes to `scripts/main.py`, Dockerfile changes): Stop the container (`Ctrl+C`), rebuild the image (Step 3), and restart (Step 4).

## Deploying to Dataloop

When your app is ready for others to use, publish it to your project. Make sure `DTLPY_PROJECT_ID` is set in your `.env` file (see Step 2).

First, install the Python dependencies that `install.py` needs:

**macOS / Linux:**

```bash
pip3 install -r requirements.txt
```

**Windows:**

```bash
pip install -r requirements.txt
```

Then run the deploy script:

**macOS / Linux:**

```bash
python3 scripts/install.py
```

**Windows:**

```bash
python scripts/install.py
```

You can also pass the project ID directly instead of using `.env`: `python3 scripts/install.py --project_id YOUR_PROJECT_ID` (or `python` on Windows).

> **Auth:** The script uses your cached Dataloop login session if it's still valid. If the session has expired, it falls back to the `DTLPY_TOKEN` value from your `.env` file.

After installation, go to any dataset in your project and look for the **"Model Setup"** button in the toolbar apps area.

## Project Structure

```
example-panel-toolbar/
├── src/                       # Frontend source code (Vue.js)
│   ├── main.ts                # App entry point
│   ├── App.vue                # Main UI component
│   └── style.css              # Styles
├── scripts/                   # Backend code (Python)
│   ├── app.py                 # API server — model list/get/create/update endpoints
│   ├── login.py               # Reads .env and authenticates with Dataloop
│   ├── install.py             # Publishes and installs the app to Dataloop
│   └── main.py                # Entry point used by the platform in production
├── panels/model_configurator/ # Pre-built frontend (used in production)
├── dataloop.json              # App manifest — defines the panel, toolbar, and service
├── local.Dockerfile           # Docker image for local development
├── nginx.conf                 # Routes HTTPS traffic to frontend and backend
├── start_dev.sh               # Startup script that runs inside the container
├── env.example                # Template for your .env file
├── package.json               # Node.js dependencies
└── vite.config.ts             # Frontend build configuration
```

## How the Panel + Toolbar Pattern Works

In Dataloop, applications are defined by a `dataloop.json` manifest. This example declares two things:

1. **A panel** named `model_configurator` with a `dialog` slot — this tells the platform "I have a UI that should open as a popup dialog."

2. **A toolbar** button named `Model Setup` placed at `datasetBrowserApps` — this tells the platform "put a button in the dataset browser that opens my panel when clicked."

The toolbar's `invoke.namespace` points to the panel's `name`, connecting the two. When a user clicks the toolbar button, the platform opens your panel in a dialog window at the configured size.

Inside the panel, your Vue.js frontend communicates with the platform through the **frame driver** (`window.dl`), which gives you access to the current project, user, theme, and platform events.

## Customization Guide

### Changing the Frontend

Edit `src/App.vue` — this is the main UI component. Vite HMR picks up changes automatically.

Key areas:
- **Template** (top of file): HTML structure using `@dataloop-ai/components` (DlSelect, DlButton, DlInput, etc.)
- **Script** (middle): Vue 3 Composition API logic — reactive state, API calls, event handlers
- **Platform integration**: `window.dl` gives you access to the current project, user, theme, and events via `@dataloop-ai/jssdk`

### Changing the Backend API

Add routes in `scripts/app.py`. The existing endpoints (`/api/models`, `/api/models/{id}`) show the pattern. Nginx already forwards all `/api/*` requests to the Python backend, so new routes are available immediately.

### Changing the Manifest

`dataloop.json` controls how your app appears in the platform:

- **`components.panels[0].supportedSlots[0].configuration.layout`** — dialog size (`width`, `height`) and behavior (`resizeable`)
- **`components.toolbars[0].displayName`** — the label shown on the toolbar button
- **`components.toolbars[0].location`** — where the button appears (e.g. `datasetBrowserApps`)
- **`components.toolbars[0].icon`** — the icon on the toolbar button (e.g. `icon-dl-pipeline`)
- **`components.services[0].runtime`** — production resource allocation (pod type, replicas)

### Adding Dependencies

- **Frontend (npm)**: Add to `package.json`, then restart the container (the startup script runs `npm install`)
- **Backend (pip)**: Add to both `Dockerfile` and `local.Dockerfile`, then rebuild the image (`docker build`)

### Rebuilding the Production Frontend

```bash
npm run build
```

This outputs compiled files to `panels/model_configurator/`. These files are included in the DPK when you run `install.py`.

## Troubleshooting

| What you see | What to do |
|---|---|
| Browser shows "400 Bad Request" | You used `http://` instead of `https://`. Change the URL to start with `https://`. |
| Browser shows a certificate warning | This is expected. Click through the warning (see Step 5). |
| `login.py` crashes with a token error | Your token may be expired. Repeat Step 1 to get a fresh one, update `.env`, and restart the container. |
| Container exits immediately after starting | Check that `.env` exists and has both `DTLPY_ENV` and `DTLPY_TOKEN` filled in. |
| `docker build` fails downloading the base image | The base image is hosted on `hub.dataloop.ai` which may require authentication. Try removing `--pull` from the build command if present. |
| Port 3004 is already in use | Another container or process is using that port. Run `docker ps` to find it, then `docker stop <container_id>`. |
| No models appear in the dropdown | Your Dataloop project may not have any models yet. Create one in the platform first, or check that your token has access to the correct project. |

## Learn More

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)
- [UI Toolbars](https://developers.dataloop.ai/tutorials/applications/toolbars/chapter)
- [Dataloop Applications Overview](https://developers.dataloop.ai/tutorials/applications/introduction/chapter)
- [Dataloop SDK Documentation](https://developers.dataloop.ai)
