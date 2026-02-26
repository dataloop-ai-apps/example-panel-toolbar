import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger('[Route Slot Example]')
logging.basicConfig(level='INFO')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
