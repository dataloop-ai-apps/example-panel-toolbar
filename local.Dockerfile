FROM docker.io/dataloopai/dtlpy-agent:cpu.py3.10.opencv

USER root

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Generate SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/local.dataloop.ai.key \
    -out /etc/ssl/certs/local.dataloop.ai.crt \
    -subj "/CN=local.dataloop.ai"

WORKDIR /tmp/app

RUN pip install --no-cache-dir \
    dtlpy>=1.90.0 \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    aiofiles>=23.0.0 \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0 \
    typing-extensions>=4.5.0

# Set the default command to run start_dev.sh (available via volume mount)
CMD ["bash", "-c", "chmod +x /tmp/app/start_dev.sh && ./start_dev.sh"]