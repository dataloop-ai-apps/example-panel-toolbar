# Dataloop UI Application Examples

Example applications demonstrating how to build and deploy UI apps on the [Dataloop](https://dataloop.ai) platform. Each example showcases a different application slot type.

## Examples

| Example | Slot Type | Description |
|---|---|---|
| [Panel + Toolbar](./example-panel-toolbar/) | `dialog` + toolbar | A popup panel triggered by a toolbar button in the dataset browser |
| [Route Slot](./example-route-slot/) | `route` | A full-page application accessible from the platform sidebar |

## Quick Start

Each example is a self-contained project. Navigate into any example directory and follow its README:

```bash
cd example-panel-toolbar   # or example-route-slot
```

### Local Development (Docker)

```bash
docker build --pull --rm -f 'local.Dockerfile' -t 'my-app:latest' '.'
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" my-app:latest
```

### Platform Deployment

```bash
python scripts/install.py -project_id YOUR_PROJECT_ID
```

## Slot Types Overview

| Slot Type | Trigger | Display | Best For |
|---|---|---|---|
| `dialog` + toolbar | Toolbar button click | Popup dialog (configurable size) | Quick actions, configuration panels |
| `route` | Sidebar navigation icon | Full page | Dashboards, full applications |

## Prerequisites

- Python 3.10+
- Docker
- Node.js 16+
- Dataloop account and project

## Documentation

- [Building Web Apps on Dataloop](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)
- [Dataloop SDK Documentation](https://developers.dataloop.ai)
