from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import Optional, Any
import json
import threading
import time

# Importar a BRX Engine
from brx_engine_core import BRXOrchestrator, Vector3

app = FastAPI(
    title="BRX Gateway API",
    description="API para interação de IA com a BRX Engine em tempo real (Live Programming)",
    version="1.0.0"
)

# Referência global ao BRXOrchestrator
engine_instance = None

# --- Modelos Pydantic para Requisições e Respostas ---

class Vector3Model(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class CreateEntityRequest(BaseModel):
    type: str
    name: Optional[str] = None
    position: Optional[Vector3Model] = Vector3Model()
    rotation: Optional[Vector3Model] = Vector3Model()
    scale: Optional[Vector3Model] = Vector3Model(x=1.0, y=1.0, z=1.0)

class SetPropertyRequest(BaseModel):
    entity_id: str
    property_name: str
    property_value: Any

class GetPropertyRequest(BaseModel):
    entity_id: str
    property_name: str

class ExecuteActionRequest(BaseModel):
    action_name: str
    parameters: Optional[dict] = {}

class APIResponse(BaseModel):
    status: str
    message: str
    entity_id: Optional[str] = None
    property_value: Optional[Any] = None
    result: Optional[Any] = None

# --- Inicialização da Engine ---

def initialize_engine():
    """Inicializa a BRX Engine em modo headless (sem renderização OpenGL)."""
    global engine_instance
    engine_instance = BRXOrchestrator(headless=True)
    
    # Executar a engine em uma thread separada
    engine_thread = threading.Thread(target=engine_instance.run, daemon=True)
    engine_thread.start()
    
    # Aguardar um pouco para garantir que a engine está pronta
    time.sleep(0.5)

@app.on_event("startup")
async def startup_event():
    """Inicializa a engine quando a API inicia."""
    initialize_engine()

# --- Endpoints da API ---

@app.post("/brx/entity/create", response_model=APIResponse, summary="Cria uma nova entidade na BRX Reality")
async def create_entity(request: CreateEntityRequest):
    """Cria uma nova entidade (objeto) na cena com propriedades iniciais."""
    if engine_instance is None:
        raise HTTPException(status_code=500, detail="BRX Engine não inicializada.")
    
    try:
        properties = {
            "position": request.position.dict(),
            "rotation": request.rotation.dict(),
            "scale": request.scale.dict()
        }
        
        entity_id = engine_instance.create_entity(
            request.type,
            request.name,
            **properties
        )
        
        return APIResponse(
            status="success",
            message=f"Entidade {request.type} criada com sucesso.",
            entity_id=entity_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/brx/entity/set_property", response_model=APIResponse, summary="Define uma propriedade para uma entidade existente")
async def set_entity_property(request: SetPropertyRequest):
    """Define uma propriedade de uma entidade existente (ex: posição, rotação, cor)."""
    if engine_instance is None:
        raise HTTPException(status_code=500, detail="BRX Engine não inicializada.")
    
    try:
        success = engine_instance.set_entity_property(
            request.entity_id,
            request.property_name,
            request.property_value
        )
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Entidade '{request.entity_id}' não encontrada.")
        
        return APIResponse(
            status="success",
            message=f"Propriedade '{request.property_name}' da entidade '{request.entity_id}' definida com sucesso."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/brx/entity/get_property", response_model=APIResponse, summary="Obtém o valor de uma propriedade de uma entidade")
async def get_entity_property(entity_id: str, property_name: str):
    """Obtém o valor atual de uma propriedade de uma entidade."""
    if engine_instance is None:
        raise HTTPException(status_code=500, detail="BRX Engine não inicializada.")
    
    try:
        value = engine_instance.get_entity_property(entity_id, property_name)
        
        if value is None:
            raise HTTPException(status_code=404, detail=f"Propriedade '{property_name}' não encontrada para a entidade '{entity_id}'.")
        
        return APIResponse(
            status="success",
            message=f"Propriedade '{property_name}' da entidade '{entity_id}' obtida com sucesso.",
            property_value=value
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/brx/scene/state", response_model=dict, summary="Obtém o estado atual da cena (Live View)")
async def get_scene_state():
    """Retorna o estado completo da cena, incluindo todas as entidades e suas propriedades."""
    if engine_instance is None:
        raise HTTPException(status_code=500, detail="BRX Engine não inicializada.")
    
    try:
        scene_state = engine_instance.get_scene_state()
        return {
            "status": "success",
            "scene": scene_state
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/brx/action/execute", response_model=APIResponse, summary="Executa uma ação genérica na engine")
async def execute_action(request: ExecuteActionRequest):
    """Executa uma ação pré-definida na engine (ex: start_game, pause_game)."""
    if engine_instance is None:
        raise HTTPException(status_code=500, detail="BRX Engine não inicializada.")
    
    try:
        if request.action_name == "start_game":
            message = "Jogo iniciado com sucesso!"
            result = {"status": "running"}
        elif request.action_name == "pause_game":
            message = "Jogo pausado."
            result = {"status": "paused"}
        elif request.action_name == "stop_game":
            engine_instance.running = False
            message = "Jogo parado."
            result = {"status": "stopped"}
        else:
            raise HTTPException(status_code=400, detail=f"Ação '{request.action_name}' desconhecida.")
        
        return APIResponse(
            status="success",
            message=message,
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/brx/health", summary="Verifica a saúde da API e da Engine")
async def health_check():
    """Verifica se a API e a Engine estão funcionando corretamente."""
    return {
        "status": "healthy",
        "engine_running": engine_instance.running if engine_instance else False,
        "message": "BRX Gateway está operacional."
    }

@app.get("/brx/tools", summary="Retorna a lista de ferramentas disponíveis para IAs")
async def get_tools():
    """Retorna o manifesto de ferramentas (Tool Definitions) para que IAs entendam os comandos disponíveis."""
    tools = [
        {
            "name": "create_entity",
            "description": "Cria uma nova entidade (objeto 3D) na cena da BRX Engine",
            "endpoint": "POST /brx/entity/create",
            "parameters": {
                "type": "string (ex: 'BRXCube', 'BRXCamera')",
                "name": "string (opcional)",
                "position": "object {x, y, z}",
                "rotation": "object {x, y, z}",
                "scale": "object {x, y, z}"
            }
        },
        {
            "name": "set_property",
            "description": "Define uma propriedade de uma entidade existente",
            "endpoint": "POST /brx/entity/set_property",
            "parameters": {
                "entity_id": "string",
                "property_name": "string (ex: 'position', 'rotation', 'color')",
                "property_value": "any"
            }
        },
        {
            "name": "get_property",
            "description": "Obtém o valor de uma propriedade de uma entidade",
            "endpoint": "GET /brx/entity/get_property",
            "parameters": {
                "entity_id": "string",
                "property_name": "string"
            }
        },
        {
            "name": "get_scene_state",
            "description": "Obtém o estado completo da cena (Live View)",
            "endpoint": "GET /brx/scene/state",
            "parameters": {}
        },
        {
            "name": "execute_action",
            "description": "Executa uma ação na engine",
            "endpoint": "POST /brx/action/execute",
            "parameters": {
                "action_name": "string (ex: 'start_game', 'pause_game')",
                "parameters": "object (opcional)"
            }
        }
    ]
    return {
        "status": "success",
        "tools": tools,
        "message": "Use essas ferramentas para programar a BRX Engine em tempo real."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
