FROM hub.dataloop.ai/dtlpy-runner-images/cpu:python3.10_opencv

# Install required packages explicitly
RUN pip install --no-cache-dir \
    dtlpy==1.98.19 \
    fastapi==0.115.12 \
    uvicorn[standard]==0.34.0 \
    aiofiles==24.1.0 \
    pydantic==2.11.1 \
    typing-extensions==4.13.1
