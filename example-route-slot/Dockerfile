FROM hub.dataloop.ai/dtlpy-runner-images/cpu:python3.10_opencv

# Install required packages explicitly
RUN pip install --no-cache-dir \
    dtlpy>=1.90.0 \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    aiofiles>=23.0.0 \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0 \
    typing-extensions>=4.5.0
