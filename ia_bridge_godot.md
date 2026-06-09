# IA-Bridge para o Código-Fonte da Godot Engine

Este documento serve como uma ponte para facilitar a interação de IAs (como o Codex) com o código-fonte da Godot Engine, localizado em `/home/ubuntu/godot_source`. O objetivo é permitir que a IA compreenda a estrutura, localize componentes chave e proponha modificações ou extensões de forma eficiente para a criação da BRX Engine.

## 1. Estrutura de Diretórios da Godot (Visão Geral)

A Godot Engine possui uma estrutura de diretórios modular. Os principais diretórios de interesse são:

-   `core/`: Contém as classes fundamentais da engine, como `Object`, `Node`, `Resource`, `String`, `Vector`, etc. É o coração da engine.
-   `scene/`: Contém as classes relacionadas à árvore de cena, nós 2D e 3D, como `Node2D`, `Node3D` (anteriormente `Spatial`), `Camera2D`, `Camera3D`, `MeshInstance3D`, etc.
-   `servers/`: Implementa os 
servidores de baixo nível (rendering, physics, audio, etc.).
-   `platform/`: Contém o código específico para cada plataforma (Windows, Linux, macOS, Android, iOS, Web).
-   `modules/`: Contém módulos opcionais que estendem a funcionalidade da engine (ex: GDScript, C#, etc.).

## 2. Ferramentas para Navegação e Busca (para Codex)

Para auxiliar na navegação e compreensão do código, o Codex pode utilizar o script `godot_explorer.py`:

-   **Listar arquivos em um módulo:**
    ```bash
    python /home/ubuntu/godot_explorer.py list_module /home/ubuntu/godot_source/core
    ```
    Isso listará todos os arquivos dentro do diretório `core/`.

-   **Encontrar definição de classe:**
    ```bash
    python /home/ubuntu/godot_explorer.py find_class /home/ubuntu/godot_source Node
    ```
    Isso buscará a definição da classe `Node` nos arquivos `.h`, `.cpp` e `.py` a partir do diretório `/home/ubuntu/godot_source`.

## 3. Diretrizes para Modificação e Extensão (BRX Engine)

Ao modificar o código da Godot para a BRX Engine, o Codex deve seguir as seguintes diretrizes:

-   **Foco em 3D:** Priorizar a análise e modificação de componentes relacionados a `Node3D` (anteriormente `Spatial`), `Camera3D`, `MeshInstance3D`, e os servidores de renderização e física 3D.
-   **Abstração:** Manter a arquitetura modular da Godot. Se uma nova funcionalidade for adicionada, ela deve ser encapsulada em uma nova classe ou módulo, seguindo os padrões existentes.
-   **Compatibilidade:** Ao introduzir novas funcionalidades, considerar a compatibilidade com hardware mais antigo (como a Intel HD Graphics 3000 do usuário), preferindo abordagens que não exijam OpenGL 4.0+ ou recursos de shader muito avançados inicialmente.
-   **Documentação:** Sempre que uma modificação significativa for feita ou uma nova funcionalidade for adicionada, o Codex deve gerar ou atualizar a documentação relevante, explicando o propósito, uso e impacto da mudança.
-   **Testes:** Propor a criação de testes unitários ou de integração para as novas funcionalidades, garantindo a estabilidade da engine.

## 4. Próximos Passos para o Codex

1.  **Analisar `core/` e `scene/`:** Começar explorando os diretórios `core/` e `scene/` para entender as classes base de objetos e a estrutura da árvore de cena 3D.
2.  **Identificar o Renderizador 3D:** Localizar o código responsável pela renderização 3D (provavelmente em `servers/rendering/`) para entender como os objetos são desenhados na tela.
3.  **Propor um Plano de Modificação:** Com base na análise, o Codex deve propor um plano detalhado para adaptar a Godot para a BRX Engine, focando nas necessidades específicas de jogos 3D e na otimização para IAs.

Este documento será expandido conforme a BRX Engine evolui, servindo como um guia contínuo para o desenvolvimento assistido por IA.
