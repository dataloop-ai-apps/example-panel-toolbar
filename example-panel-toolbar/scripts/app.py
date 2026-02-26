import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import os
from pathlib import Path

import dtlpy as dl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger('[Model Configurator]')
logging.basicConfig(level='INFO')

# Simple models
class ModelData(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    configuration: Dict[str, Any] = {}
    base_model_id: Optional[str] = None
    project_id: str

class ModelUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

class ModelResponse(BaseModel):
    id: str
    name: str
    type: str
    description: str
    configuration: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    project_id: str

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/models")
async def list_models(project_id: str) -> List[ModelResponse]:
    """Get all models in project"""
    logger.info(f"Listing models for project: {project_id}")
    
    project = dl.projects.get(project_id=project_id)
    models_pages = project.models.list()
    
    response = []
    for page in models_pages:
        for model in page:
            response.append(ModelResponse(
                id=model.id,
                name=model.name,
                type=getattr(model, 'model_type', 'custom'),
                description=getattr(model, 'description', ''),
                configuration=getattr(model, 'configuration', {}),
                created_at=getattr(model, 'created_at', None),
                project_id=project.id
            ))
    
    logger.info(f"Found {len(response)} models")
    return response

@app.get("/api/models/{model_id}")
async def get_model(model_id: str) -> ModelResponse:
    """Get single model"""
    model = dl.models.get(model_id=model_id)
    
    return ModelResponse(
        id=model.id,
        name=model.name,
        type=getattr(model, 'model_type', 'custom'),
        description=getattr(model, 'description', ''),
        configuration=getattr(model, 'configuration', {}),
        created_at=getattr(model, 'created_at', None),
        project_id=getattr(model.project, 'id', '') if hasattr(model, 'project') else ''
    )

@app.post("/api/models")
async def create_model(model_data: ModelData) -> ModelResponse:
    """Create new model by cloning"""
    logger.info(f"Creating model: {model_data.name}")
    
    project = dl.projects.get(project_id=model_data.project_id)
    base_model = dl.models.get(model_id=model_data.base_model_id)
    
    cloned_model = base_model.clone(
        model_name=model_data.name,
        configuration=model_data.configuration,
        description=model_data.description or f"Cloned from {base_model.name}",
        project_id=model_data.project_id,
        wait=False
    )
    
    logger.info(f"Model created: {cloned_model.id}")
    
    return ModelResponse(
        id=cloned_model.id,
        name=cloned_model.name,
        type=getattr(cloned_model, 'model_type', 'custom'),
        description=cloned_model.description,
        configuration=getattr(cloned_model, 'configuration', {}),
        created_at=datetime.now(),
        project_id=project.id
    )

@app.put("/api/models/{model_id}")
async def update_model(model_id: str, update_data: ModelUpdate) -> ModelResponse:
    """Update existing model"""
    logger.info(f"Updating model: {model_id}")
    
    model = dl.models.get(model_id=model_id)
    
    if update_data.name:
        model.name = update_data.name
    if update_data.description:
        model.description = update_data.description
    if update_data.configuration:
        model.configuration = update_data.configuration
    
    model = model.update()
    
    return ModelResponse(
        id=model.id,
        name=model.name,
        type=getattr(model, 'model_type', 'custom'),
        description=getattr(model, 'description', ''),
        configuration=getattr(model, 'configuration', {}),
        created_at=getattr(model, 'created_at', None),
        project_id=getattr(model.project, 'id', '') if hasattr(model, 'project') else ''
    )


# Get the project root directory (parent of scripts directory)
project_root = Path(__file__).parent.parent
panels_dir = project_root / "panels" / "model_configurator"

app.mount(
    "/model_configurator", 
    StaticFiles(directory=str(panels_dir), html=True), 
    name='model_configurator'
)

