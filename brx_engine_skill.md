# Skill: BRX Engine Developer

Esta skill capacita o Codex a desenvolver, modificar e otimizar a BRX Engine, uma engine de jogos 3D baseada no código-fonte da Godot Engine. O foco principal é a criação de jogos 3D com perspectiva completa (6 eixos) e a otimização para hardware legado, como a Intel HD Graphics 3000.

## Capacidades da Skill:

*   **Exploração de Código**: Navegar e compreender a estrutura modular da Godot Engine.
*   **Identificação de Componentes**: Localizar classes, módulos e servidores relevantes para renderização 3D, física e entrada.
*   **Modificação e Extensão**: Propor e implementar alterações no código-fonte para adaptar a Godot à visão da BRX Engine.
*   **Otimização para Hardware Legado**: Adaptar o código para garantir compatibilidade e performance em GPUs mais antigas (OpenGL 2.1/3.0).
*   **Geração de Código**: Criar novos componentes, nós de cena e funcionalidades seguindo os padrões da BRX Engine.
*   **Documentação**: Gerar e atualizar documentação técnica para as modificações e novas funcionalidades.

## Contexto e Ferramentas:

O Codex deve utilizar os seguintes recursos para interagir com o projeto:

*   **Repositório Base**: `/home/ubuntu/BRX_ENGINER_REPO/` (contém o código-fonte da Godot).
*   **Guia de Arquitetura (IA-Bridge)**: `/home/ubuntu/BRX_ENGINER_REPO/ia_bridge_godot.md` - Este documento detalha a arquitetura da Godot e as diretrizes para a BRX Engine.
*   **Explorador de Código**: `/home/ubuntu/BRX_ENGINER_REPO/godot_explorer.py` - Script Python para listar módulos e encontrar definições de classes no código-fonte.
*   **Fluxo de Trabalho**: `/home/ubuntu/BRX_ENGINER_REPO/BRX_ENGINE_WORKFLOW.md` - Guia geral de como colaborar no projeto.

## Comandos Essenciais (Exemplos):

*   **Listar arquivos de um módulo**: `python3 /home/ubuntu/BRX_ENGINER_REPO/godot_explorer.py list_module /home/ubuntu/BRX_ENGINER_REPO/core`
*   **Encontrar definição de classe**: `python3 /home/ubuntu/BRX_ENGINER_REPO/godot_explorer.py find_class /home/ubuntu/BRX_ENGINER_REPO Node3D`
*   **Compilar a Engine**: `cd /home/ubuntu/BRX_ENGINER_REPO && scons platform=linuxbsd target=editor dev_build=yes`

## Diretrizes de Desenvolvimento:

1.  **Foco 3D**: Priorizar o desenvolvimento e otimização de funcionalidades 3D. A BRX Engine deve ser robusta para ambientes tridimensionais complexos.
2.  **Modularidade**: Manter a estrutura modular da Godot. Novas funcionalidades devem ser adicionadas de forma organizada, preferencialmente em novos módulos ou classes.
3.  **Performance**: Sempre considerar a performance, especialmente para GPUs integradas. Otimizações de renderização e física são cruciais.
4.  **Documentação Contínua**: Cada alteração ou adição significativa deve ser acompanhada de atualização na documentação, explicando o "porquê" e o "como".

Esta skill é a sua porta de entrada para construir a BRX Engine com o Codex.
