# Dataloop UI Application Examples

Two working examples that show you how to build custom web applications for the [Dataloop](https://dataloop.ai) platform. Pick the one that matches what you want to build, follow the steps, and you'll have a running app.

## Which Example Should I Use?

| If you want to... | Use this example | What it looks like |
|---|---|---|
| Add a **popup button** to the dataset browser (e.g. a settings panel, a quick action) | [Panel + Toolbar](./example-panel-toolbar/) | A button appears in the dataset toolbar. Clicking it opens a popup dialog. |
| Add a **full page** to the platform sidebar (e.g. a dashboard, a standalone tool) | [Route Slot](./example-route-slot/) | An icon appears in the left sidebar. Clicking it opens your app as a full page. |

## Before You Start

You need four things:

1. **Docker Desktop** installed and running ([download](https://www.docker.com/products/docker-desktop/))
2. **Python 3.10 or newer** installed ([download](https://www.python.org/downloads/))
3. **A Dataloop account** — sign up free at [console.dataloop.ai](https://console.dataloop.ai)
4. **A Dataloop project** — after signing up, create a project from the console home page

You do **not** need to install Node.js on your own machine. The Docker container handles that.

## Getting Started

Each example has its own README with step-by-step setup instructions:

- **[Panel + Toolbar README](./example-panel-toolbar/README.md)** — popup dialog triggered by a toolbar button
- **[Route Slot README](./example-route-slot/README.md)** — full page accessed from the sidebar

Both examples follow the same workflow: get a token, create `.env`, build a Docker image, and start the container.

## How the Local Dev Environment Works

When you run the Docker container, three services start inside it:

```
Your browser
  └── https://localhost:3004
        └── Nginx (handles HTTPS, routes traffic)
              ├── /api requests  →  Python backend (FastAPI + Dataloop SDK)
              └── everything else →  Vue.js frontend (Vite with live reload)
```

Your project folder is mounted into the container, so any changes you make to the frontend code (`src/` folder) will appear in the browser immediately without restarting anything.

## Deploying to the Dataloop Platform

Once your app works locally, you can publish it to your Dataloop project so other team members can use it. Each example README has deployment instructions — run `scripts/install.py` from inside the example directory. The script reads credentials from your `.env` file.

## Learn More

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter) — official tutorial
- [Dataloop Applications Overview](https://developers.dataloop.ai/tutorials/applications/introduction/chapter) — how panels, toolbars, and slots work
- [Dataloop SDK Documentation](https://developers.dataloop.ai) — full Python SDK reference
