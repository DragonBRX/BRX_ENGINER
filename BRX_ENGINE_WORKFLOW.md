# Fluxo de Trabalho: BRX Engine + Codex

Este guia define como você e seu Codex (com suas 1.600+ skills) devem colaborar para transformar o código da Godot na **BRX Engine**.

## 1. Preparação do Ambiente
O código-fonte da Godot já foi clonado em `/home/ubuntu/godot_source`. Este é o seu "laboratório".

## 2. Como usar o Codex com a BRX Engine
Para que o Codex seja eficaz, ele deve carregar a nova skill que criamos:
1.  **Carregar Skill:** Peça ao Codex para ler o arquivo `/home/ubuntu/brx_engine_skill.json`.
2.  **Exploração Assistida:** Use comandos como `explore core` ou `find_class Node3D` para que o Codex entenda as partes específicas do motor.
3.  **Modificação:** Ao pedir uma mudança (ex: "Melhore a performance da câmera 3D"), o Codex deve consultar o `ia_bridge_godot.md` para garantir que a mudança siga a arquitetura correta.

## 3. Comandos de Build (Compilação)
A BRX Engine (Godot modificada) utiliza o `SCons` para compilação. O Codex pode executar:
```bash
cd /home/ubuntu/godot_source && scons platform=linuxbsd target=editor dev_build=yes
```
*Nota: Para o seu Pavilion G4, o Codex deve sempre verificar se as flags de otimização para OpenGL legado estão ativas.*

## 4. Integração de Novas Skills
Como você tem 1.600 skills, você pode pedir ao Codex:
> "Codex, use sua skill de [NOME DA SKILL] para analisar o módulo de física em `/home/ubuntu/godot_source/servers/physics_3d` e sugerir uma melhoria para a BRX Engine."

## 5. Arquivos Gerados nesta Sessão
| Arquivo | Função |
| :--- | :--- |
| `/home/ubuntu/godot_source/` | Código-fonte base (Godot Engine) |
| `brx_engine_skill.json` | Definição da skill para o seu Codex |
| `ia_bridge_godot.md` | Manual de arquitetura para a IA |
| `godot_explorer.py` | Ferramenta de busca de classes e módulos |
| `brx_engine_core.py` | Protótipo funcional em Python para testes rápidos |

---
**Manus AI** - Criando a base para a próxima geração de engines 3D.
