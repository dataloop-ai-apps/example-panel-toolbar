# Example Panel Toolbar - Model Configurator

A demo application for configuring machine learning models in the Dataloop platform. This UI panel allows users to select models, modify their configurations, and create new models by cloning existing ones.

## Features

- 🔍 **Model Selection**: Browse and select from available models in your project
- ⚙️ **Configuration Editor**: Edit model parameters with different input types (text, number, checkbox, JSON)
- 🔄 **Model Cloning**: Create new models by cloning existing ones with modified configurations
- 💾 **Configuration Updates**: Save changes to existing model configurations

## Local Development Setup

### Prerequisites

- Python 3.8+
- Docker
- Node.js 16+ (for frontend development)
- Dataloop account and project

### Step 1: Dataloop Authentication

First, you need to authenticate with Dataloop and get your access token:

```bash
# Install Dataloop SDK if not already installed
pip install dtlpy

# Start Python interactive session
python3
```

```python
import dtlpy as dl

# Set your environment (production, rc, etc.)
dl.setenv('prod')  # or 'rc' for staging

# Login to Dataloop
dl.login()

# Get your access token
token = dl.token()
print(f"Your token: {token}")
```

### Step 2: Environment Setup

Create a `.env` file in the project root with your Dataloop token:

```bash
# Copy the example file and edit it
cp env.example .env

# Edit .env with your actual values
# .env file should contain:
DTLPY_ENV=PROD
DATALOOP_TOKEN=your_token_here
```

### Step 3: Docker Build and Run

#### Build the Docker Image

**macOS (Apple Silicon):**

```bash
docker build --platform linux/amd64 --pull --rm -f 'local.Dockerfile' -t 'examplepaneltoolbar:latest' '.'
```

**macOS (Intel) / Linux / Unix:**

```bash
docker build --pull --rm -f 'local.Dockerfile' -t 'examplepaneltoolbar:latest' '.'
```

**Windows (Command Prompt):**

```cmd
docker build --pull --rm -f local.Dockerfile -t examplepaneltoolbar:latest .
```

#### Run the Container

**macOS (Apple Silicon):**

```bash
# Using current directory
docker run  --platform linux/amd64  -p 3004:3000 -it -v "$(pwd):/tmp/app" examplepaneltoolbar:latest
```

**macOS (Intel) / Linux / Unix:**

```bash
# Using current directory
docker run -p 3004:3000 -it -v "$(pwd):/tmp/app" examplepaneltoolbar:latest
```

**Windows (Command Prompt):**

```bash
# Using current directory
docker run -p 3004:3000 -it -v "%cd%:/tmp/app" examplepaneltoolbar:latest
```

### Step 4: Access the Application

Once the container is running, the application will be available at:

```
http://localhost:3004/model_configurator
```

### Additional Setup

For running local development, please see instructions here [Building Web Apps](https://developers.dataloop.ai/tutorials/applications/web_application/chapter)

## Platform Deployment

### Prerequisites for Platform Installation

1. **Environment Setup**: Create a `.env` file with your Dataloop credentials:

   ```bash
   # Copy the example file and edit it
   cp env.example .env

   # Edit .env with your actual values:
   DTLPY_ENV=prod
   DATALOOP_TOKEN=your_token_here
   ```

### Install in Your Project

To install this app in your Dataloop project, use the install script with your project ID:

```bash
# Install the app in your project
python scripts/install.py -project_id YOUR_PROJECT_ID

```

The install script will:

- Connect to your Dataloop environment
- Publish the app package (DPK)
- Install or update the app in your specified project
