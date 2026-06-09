# Mapeamento Mestre da BRX Engine (Base Godot)

Este documento serve como o mapa completo da arquitetura da BRX Engine, baseada no código-fonte da Godot Engine. Ele detalha a função de cada diretório principal e como eles devem ser abordados para a criação e modificação da engine, com foco em 3D e otimização para IAs (Codex).

## Estrutura Principal

A BRX Engine herda a estrutura modular da Godot. Abaixo estão os diretórios mais críticos para o desenvolvimento:

### 1. `core/` (O Coração da Engine)
Este diretório contém as fundações da engine. É aqui que os tipos básicos, a matemática e o sistema de objetos são definidos.

*   **`core/math/`**: Contém as classes matemáticas essenciais, como `Vector3`, `Matrix3`, `Quaternion`, etc. **Para a BRX Engine**, este módulo é crucial para garantir a precisão das transformações 3D (os 6 eixos de movimento).
*   **`core/object/`**: Define a classe base `Object`, da qual quase tudo na engine herda.
*   **`core/variant/`**: Implementa o tipo `Variant`, usado para tipagem dinâmica e comunicação entre scripts e C++.
*   **`core/io/`**: Lida com entrada e saída de arquivos, rede e serialização.

### 2. `scene/` (A Árvore de Cena)
Este diretório contém os nós (Nodes) que compõem os jogos.

*   **`scene/3d/`**: O foco principal da BRX Engine. Contém nós como `Node3D` (base para objetos 3D), `Camera3D`, `MeshInstance3D`, luzes e colisores 3D. **Modificações aqui** definirão como os objetos se comportam e interagem no espaço 3D.
*   **`scene/2d/`**: Contém os nós 2D. Embora a BRX Engine foque em 3D, o suporte 2D é mantido para interfaces (UI) e jogos mistos.
*   **`scene/gui/`**: Contém os controles de interface de usuário (botões, painéis, etc.).
*   **`scene/animation/`**: Sistema de animação para propriedades e esqueletos 3D.

### 3. `servers/` (Os Servidores de Baixo Nível)
Os servidores lidam com as tarefas pesadas de forma assíncrona.

*   **`servers/rendering/`**: O servidor de renderização. É aqui que a mágica visual acontece. **Para a BRX Engine (foco em Intel HD 3000)**, este é o local para otimizar shaders e garantir que o pipeline de renderização (provavelmente o GLES3/OpenGL) seja eficiente e compatível com hardware legado.
*   **`servers/physics_3d/`**: O servidor de física 3D. Lida com colisões, gravidade e dinâmicas de corpos rígidos.
*   **`servers/audio/`**: Gerencia a reprodução e mixagem de áudio.

### 4. `modules/` (Extensões)
Módulos adicionam funcionalidades extras à engine.

*   **`modules/gdscript/`**: A linguagem de script padrão da Godot.
*   **Outros Módulos**: A BRX Engine pode adicionar novos módulos aqui para integrar ferramentas de IA ou suporte a outras linguagens de forma nativa.

### 5. `platform/` (Plataformas Alvo)
Contém o código específico para compilar a engine para diferentes sistemas operacionais (Windows, Linux, macOS, Android, etc.).

## Como o Codex Deve Usar Este Mapa

1.  **Identificar o Objetivo**: Quando solicitado a criar ou modificar algo (ex: "Melhorar a câmera 3D"), o Codex deve consultar este mapa para saber onde procurar (neste caso, `scene/3d/` e possivelmente `core/math/`).
2.  **Explorar o Código**: Usar o `godot_explorer.py` para listar os arquivos dentro do diretório identificado e encontrar as classes relevantes.
3.  **Propor Modificações**: Com base na compreensão da arquitetura, propor as alterações no código C++ ou Python, garantindo que elas se integrem perfeitamente à estrutura existente.
4.  **Otimizar**: Sempre ter em mente as diretrizes de otimização (especialmente para renderização em `servers/rendering/`) para garantir a performance no hardware alvo.

Este mapa é vivo e deve ser atualizado conforme a BRX Engine evolui e novos componentes são adicionados.
