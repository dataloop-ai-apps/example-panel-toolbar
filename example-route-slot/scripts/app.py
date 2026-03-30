import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger('[Route Slot Example]')
logging.basicConfig(level='INFO')

app = FastAPI()

ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "https://console.dataloop.ai,https://gate.dataloop.ai"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


project_root = Path(__file__).parent.parent
panels_dir = project_root / "panels" / "route-slot"

app.mount(
    "/route-slot",
    StaticFiles(directory=str(panels_dir), html=True),
    name='route-slot'
)
