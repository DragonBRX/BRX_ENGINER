## Plano de Renomeação da BRX Engine

Este documento detalha as renomeações realizadas nos componentes da BRX Engine para remover termos genéricos e aprimorar a identidade da engine, tornando-a mais clara e amigável para programação por IAs.

### Renomeações de Diretórios:

*   `core/` renomeado para `brxkernel/`
*   `modules/` renomeado para `brxextensions/`
*   `main/` renomeado para `brxorchestrator/`
*   `scene/` renomeado para `brxreality/`
*   `drivers/` renomeado para `brxadapters/`
*   `servers/` renomeado para `brxservices/`
*   `editor/` renomeado para `brxforge/`

### Atualizações em Arquivos:

*   **SConstruct**: Referências a `core/`, `modules/`, `main/`, `scene/`, `drivers/`, `servers/`, `editor/` foram atualizadas para `brxkernel/`, `brxextensions/`, `brxorchestrator/`, `brxreality/`, `brxadapters/`, `brxservices/`, `brxforge/` respectivamente.
*   **brxorchestrator/main.cpp**: Referências a `core/`, `modules/`, `scene/`, `drivers/`, `servers/`, `editor/` foram atualizadas para `brxkernel/`, `brxextensions/`, `brxreality/`, `brxadapters/`, `brxservices/`, `brxforge/` respectivamente.
*   **version.py**: `short_name` atualizado para `BRX` e `name` para `BRX Engine`.
*   **brx_engine_architecture.md**: Termos genéricos como "Núcleo", "Módulos", "Sistema de Renderização", "Gerenciamento de Cena", "Sistema de Input", "Sistema de Física", "Sistema de Áudio", "Sistema de Animação", "Sistema de Recursos (Assets)", "Scripting", "Servidor de Física", "Node", "Componentes", "Loop Principal (Main Loop)" foram substituídos por suas contrapartes com o prefixo `BRX` ou termos mais específicos como `BRXKernel`, `BRXExtensions`, `BRXRenderer`, `BRXReality`, `BRXInput`, `BRXPhysics`, `BRXAudio`, `BRXAnimation`, `BRXAssets`, `BRXScripting`, `BRXPhysicsServer`, `BRXNode`, `BRXComponents`, `BRXOrchestrator` e `BRXRenderAPI`.
