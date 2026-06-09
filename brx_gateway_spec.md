# Especificação do BRX Gateway (API de Conector para IA)

## 1. Introdução

O BRX Gateway é uma interface de programação de aplicações (API) projetada para permitir que modelos de Inteligência Artificial (IA) interajam e programem a BRX Engine de forma eficiente e padronizada. Ele atua como um "conector" ou "plugin", traduzindo as intenções da IA em ações executáveis dentro da engine, facilitando a criação e manipulação de mundos virtuais, lógica de jogo e elementos interativos.

## 2. Princípios de Design

*   **Simplicidade**: A API deve ser fácil de entender e usar por modelos de IA, com endpoints claros e payloads de dados intuitivos.
*   **Modularidade**: Expor funcionalidades da BRX Engine de forma modular, alinhada com a nova arquitetura (`BRXKernel`, `BRXReality`, `BRXServices`, etc.).
*   **Flexibilidade**: Suportar diferentes tipos de interações, desde a criação de objetos até a manipulação de propriedades e execução de lógicas complexas.
*   **Autodescrição**: A API deve ser capaz de descrever suas próprias capacidades, permitindo que IAs descubram e utilizem as funcionalidades disponíveis dinamicamente.
*   **JSON-centric**: Utilizar JSON para todas as requisições e respostas, garantindo compatibilidade universal com a maioria dos modelos de IA e frameworks de comunicação.

## 3. Arquitetura Proposta

O BRX Gateway será implementado como um servidor HTTP leve, provavelmente utilizando **FastAPI** (Python) para sua facilidade de uso, performance e geração automática de documentação OpenAPI (Swagger UI). Ele se comunicará com a BRX Engine (que pode ser um processo separado ou um módulo Python integrado) para executar as ações solicitadas.

```mermaid
graph TD
    A[Modelo de IA (Ex: GPT, Claude, DeepSeek)] -->|Requisições JSON| B(BRX Gateway - Servidor FastAPI)
    B -->|Chamadas Internas/IPC| C(BRX Engine - BRXOrchestrator)
    C --> D(BRXReality, BRXServices, BRXKernel, etc.)
    D --> E[Mundo Virtual / Jogo]
    E -->|Feedback Visual/Dados| C
    C -->|Respostas JSON| B
    B -->|Respostas JSON| A
```

## 4. Endpoints da API (Exemplos Iniciais)

Esta seção descreve os endpoints iniciais que o BRX Gateway exporá. Cada endpoint representará uma "ferramenta" que a IA poderá "chamar".

### 4.1. `POST /brx/entity/create`

Cria uma nova entidade (objeto) na `BRXReality`.

*   **Descrição**: Adiciona um novo objeto ao mundo virtual com propriedades iniciais.
*   **Parâmetros de Requisição (JSON)**:
    *   `type` (string, obrigatório): O tipo de entidade a ser criada (ex: "BRXCube", "BRXSphere", "BRXLight").
    *   `name` (string, opcional): Um nome único para a entidade. Se não fornecido, será gerado automaticamente.
    *   `position` (object, opcional): Posição inicial da entidade.
        *   `x` (float, padrão: 0.0)
        *   `y` (float, padrão: 0.0)
        *   `z` (float, padrão: 0.0)
    *   `rotation` (object, opcional): Rotação inicial da entidade (em graus Euler).
        *   `x` (float, padrão: 0.0)
        *   `y` (float, padrão: 0.0)
        *   `z` (float, padrão: 0.0)
    *   `scale` (object, opcional): Escala inicial da entidade.
        *   `x` (float, padrão: 1.0)
        *   `y` (float, padrão: 1.0)
        *   `z` (float, padrão: 1.0)
*   **Resposta (JSON)**:
    *   `status` (string): "success" ou "error".
    *   `entity_id` (string): ID único da entidade criada.
    *   `message` (string): Mensagem descritiva.

### 4.2. `POST /brx/entity/set_property`

Define uma propriedade específica para uma entidade existente.

*   **Descrição**: Modifica uma propriedade (ex: posição, cor, textura) de uma entidade identificada pelo seu `entity_id`.
*   **Parâmetros de Requisição (JSON)**:
    *   `entity_id` (string, obrigatório): ID da entidade a ser modificada.
    *   `property_name` (string, obrigatório): Nome da propriedade a ser definida (ex: "position", "color", "material").
    *   `property_value` (any, obrigatório): O novo valor da propriedade. O tipo dependerá da `property_name`.
*   **Resposta (JSON)**:
    *   `status` (string): "success" ou "error".
    *   `message` (string): Mensagem descritiva.

### 4.3. `GET /brx/entity/get_property`

Obtém o valor de uma propriedade de uma entidade.

*   **Descrição**: Retorna o valor atual de uma propriedade de uma entidade.
*   **Parâmetros de Requisição (JSON)**:
    *   `entity_id` (string, obrigatório): ID da entidade.
    *   `property_name` (string, obrigatório): Nome da propriedade a ser obtida.
*   **Resposta (JSON)**:
    *   `status` (string): "success" ou "error".
    *   `property_value` (any): O valor da propriedade. (Presente apenas em caso de sucesso).
    *   `message` (string): Mensagem descritiva.

### 4.4. `POST /brx/action/execute`

Executa uma ação genérica ou um script dentro da engine.

*   **Descrição**: Permite que a IA acione comportamentos pré-definidos ou execute pequenos trechos de script (se o `BRXScriptingModule` estiver ativo).
*   **Parâmetros de Requisição (JSON)**:
    *   `action_name` (string, obrigatório): Nome da ação a ser executada (ex: "start_game", "pause_game", "load_level").
    *   `parameters` (object, opcional): Dicionário de parâmetros adicionais para a ação.
*   **Resposta (JSON)**:
    *   `status` (string): "success" ou "error".
    *   `result` (any, opcional): Resultado da execução da ação.
    *   `message` (string): Mensagem descritiva.

## 5. Considerações de Segurança e Autenticação

Para ambientes de produção, o BRX Gateway precisará de mecanismos de autenticação (ex: chaves de API, OAuth2) para controlar o acesso de IAs e garantir que apenas modelos autorizados possam interagir com a engine.

## 6. Próximos Passos

1.  Implementar o servidor FastAPI para expor esses endpoints.
2.  Conectar o FastAPI com a lógica interna da BRX Engine (via IPC ou integração direta).
3.  Gerar automaticamente um "Tool Manifest" (descrição das ferramentas) a partir da especificação OpenAPI do FastAPI, para que as IAs possam consumi-lo.

---

**Autor**: Manus AI
**Data**: Junho de 2026
