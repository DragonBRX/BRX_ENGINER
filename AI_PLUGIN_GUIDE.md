# Guia de Uso: BRX Engine como Plugin de IA (Live Programming)

## 1. Visão Geral

A **BRX Engine** foi transformada em uma plataforma compatível com conectores de Inteligência Artificial, permitindo que qualquer modelo de IA (local ou remoto) controle e programe a engine em tempo real. O **BRX Gateway** atua como a interface de comunicação entre a IA e a Engine.

## 2. Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    Modelo de IA                                 │
│         (GPT-4, Claude, DeepSeek, Gemini, etc.)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Requisições JSON
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              BRX Gateway (FastAPI)                              │
│  /brx/entity/create                                             │
│  /brx/entity/set_property                                       │
│  /brx/entity/get_property                                       │
│  /brx/scene/state                                               │
│  /brx/action/execute                                            │
│  /brx/tools (Tool Definitions)                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Integração Direta
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            BRX Engine (brx_engine_core.py)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ BRXOrchestrator (Loop Principal)                        │   │
│  │ ├── BRXReality (Gerenciamento de Cena)                  │   │
│  │ ├── BRXKernel (Núcleo)                                  │   │
│  │ ├── BRXServices (Serviços Internos)                     │   │
│  │ └── BRXAdapters (Adaptadores)                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Iniciando a BRX Engine com o Gateway

### 3.1. Instalação de Dependências

```bash
pip install fastapi uvicorn pygame PyOpenGL pydantic
```

### 3.2. Executar o BRX Gateway

```bash
python brx_gateway.py
```

A API estará disponível em `http://localhost:8000`.

### 3.3. Acessar a Documentação Interativa

Abra seu navegador e acesse:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 4. Ferramentas Disponíveis para IAs

### 4.1. Criar uma Entidade

**Endpoint**: `POST /brx/entity/create`

**Descrição**: Cria um novo objeto 3D na cena.

**Exemplo de Requisição**:
```json
{
  "type": "BRXCube",
  "name": "MyCube",
  "position": {"x": 0.0, "y": 0.0, "z": 0.0},
  "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
  "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
}
```

**Resposta**:
```json
{
  "status": "success",
  "message": "Entidade BRXCube criada com sucesso.",
  "entity_id": "brx_node_1"
}
```

### 4.2. Definir uma Propriedade

**Endpoint**: `POST /brx/entity/set_property`

**Descrição**: Modifica uma propriedade de uma entidade existente (ex: posição, rotação, cor).

**Exemplo de Requisição**:
```json
{
  "entity_id": "brx_node_1",
  "property_name": "position",
  "property_value": {"x": 5.0, "y": 2.0, "z": -3.0}
}
```

**Resposta**:
```json
{
  "status": "success",
  "message": "Propriedade 'position' da entidade 'brx_node_1' definida com sucesso."
}
```

### 4.3. Obter uma Propriedade

**Endpoint**: `GET /brx/entity/get_property`

**Descrição**: Obtém o valor atual de uma propriedade de uma entidade.

**Exemplo de Requisição**:
```
GET /brx/entity/get_property?entity_id=brx_node_1&property_name=position
```

**Resposta**:
```json
{
  "status": "success",
  "message": "Propriedade 'position' da entidade 'brx_node_1' obtida com sucesso.",
  "property_value": {"x": 5.0, "y": 2.0, "z": -3.0}
}
```

### 4.4. Obter Estado da Cena (Live View)

**Endpoint**: `GET /brx/scene/state`

**Descrição**: Retorna o estado completo da cena, incluindo todas as entidades e suas propriedades.

**Resposta**:
```json
{
  "status": "success",
  "scene": {
    "id": "brx_node_0",
    "name": "Root",
    "type": "BRXNode",
    "position": {"x": 0.0, "y": 0.0, "z": 0.0},
    "children": [
      {
        "id": "brx_node_1",
        "name": "MyCube",
        "type": "BRXCube",
        "position": {"x": 5.0, "y": 2.0, "z": -3.0},
        "rotation": {"x": 0.0, "y": 45.0, "z": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
      }
    ]
  }
}
```

### 4.5. Executar uma Ação

**Endpoint**: `POST /brx/action/execute`

**Descrição**: Executa uma ação pré-definida na engine.

**Exemplo de Requisição**:
```json
{
  "action_name": "start_game",
  "parameters": {}
}
```

**Resposta**:
```json
{
  "status": "success",
  "message": "Jogo iniciado com sucesso!",
  "result": {"status": "running"}
}
```

## 5. Exemplo de Fluxo de Programação ao Vivo

Imagine que você quer que uma IA crie um cenário de jogo em tempo real. Aqui está como seria:

### Passo 1: Criar o Cenário Base
A IA faz uma requisição para criar um cubo:
```json
POST /brx/entity/create
{
  "type": "BRXCube",
  "name": "Player",
  "position": {"x": 0.0, "y": 0.0, "z": 0.0}
}
```

### Passo 2: Verificar o Estado
A IA verifica o estado atual da cena:
```
GET /brx/scene/state
```

### Passo 3: Modificar em Tempo Real
A IA move o cubo para a direita:
```json
POST /brx/entity/set_property
{
  "entity_id": "brx_node_1",
  "property_name": "position",
  "property_value": {"x": 10.0, "y": 0.0, "z": 0.0}
}
```

### Passo 4: Criar Inimigos
A IA cria múltiplos cubos para representar inimigos:
```json
POST /brx/entity/create
{
  "type": "BRXCube",
  "name": "Enemy1",
  "position": {"x": -5.0, "y": 0.0, "z": 0.0}
}
```

Tudo isso acontece em **tempo real**, com a IA vendo o resultado de cada ação antes de executar a próxima.

## 6. Integração com Modelos de IA

### 6.1. Usando com OpenAI GPT-4

```python
import openai
import requests

openai.api_key = "sua-chave-api"

# Definir as ferramentas disponíveis
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_entity",
            "description": "Cria uma nova entidade na BRX Engine",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "name": {"type": "string"},
                    "position": {"type": "object"}
                }
            }
        }
    }
]

# Fazer uma requisição ao GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Crie um cubo na posição (5, 0, 0)"}
    ],
    tools=tools
)

# Processar a resposta e chamar a API do BRX Gateway
# ...
```

### 6.2. Usando com Claude (Anthropic)

```python
import anthropic
import requests

client = anthropic.Anthropic(api_key="sua-chave-api")

# Definir as ferramentas
tools = [
    {
        "name": "create_entity",
        "description": "Cria uma nova entidade na BRX Engine",
        "input_schema": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "name": {"type": "string"},
                "position": {"type": "object"}
            }
        }
    }
]

# Fazer uma requisição ao Claude
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "Crie um cenário com 3 cubos"}
    ]
)

# Processar a resposta e chamar a API do BRX Gateway
# ...
```

## 7. Próximos Passos

1. **Adicionar WebSockets**: Para comunicação em tempo real com menor latência.
2. **Renderização Remota**: Transmitir a visualização da cena para a IA (via streaming de vídeo).
3. **Scripting Avançado**: Permitir que IAs escrevam scripts Python que rodam dentro da engine.
4. **Persistência**: Salvar e carregar cenas criadas por IAs.

---

**Autor**: Manus AI
**Data**: Junho de 2026
