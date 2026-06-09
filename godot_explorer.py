import os
import sys

def list_module_files(module_path):
    """Lista todos os arquivos em um módulo Godot específico."""
    if not os.path.isdir(module_path):
        print(f"Erro: O caminho do módulo '{module_path}' não existe.")
        return

    print(f"Arquivos no módulo '{module_path}':")
    for root, _, files in os.walk(module_path):
        for file in files:
            print(os.path.join(root, file))

def find_class_definition(root_path, class_name):
    """Procura a definição de uma classe (ex: 'class MyClass') em arquivos C++ ou Python."""
    found_files = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(('.h', '.cpp', '.py')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            if f'class {class_name}' in line or f'struct {class_name}' in line:
                                found_files.append(filepath)
                                break
                except Exception as e:
                    print(f"Erro ao ler {filepath}: {e}")
    if found_files:
        print(f"Definição da classe '{class_name}' encontrada em:")
        for f in found_files:
            print(f)
    else:
        print(f"Definição da classe '{class_name}' não encontrada em '{root_path}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python godot_explorer.py <comando> [argumentos]")
        print("Comandos disponíveis:")
        print("  list_module <caminho_do_modulo> (ex: /home/ubuntu/godot_source/core)")
        print("  find_class <caminho_raiz_busca> <nome_da_classe> (ex: /home/ubuntu/godot_source Node)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list_module":
        if len(sys.argv) < 3:
            print("Uso: python godot_explorer.py list_module <caminho_do_modulo>")
        else:
            list_module_files(sys.argv[2])
    elif command == "find_class":
        if len(sys.argv) < 4:
            print("Uso: python godot_explorer.py find_class <caminho_raiz_busca> <nome_da_classe>")
        else:
            find_class_definition(sys.argv[2], sys.argv[3])
    else:
        print(f"Comando desconhecido: {command}")
