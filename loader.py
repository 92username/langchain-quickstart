import os


def load_docs():
    """
    Procura todos os arquivos .md dentro da pasta /docs/,
    lê e concatena o conteúdo em uma única string.

    Returns:
        str: Conteúdo combinado de todos os arquivos Markdown
    """
    folder = "docs"
    combined = ""

    # Verificar se a pasta existe, criar se não existir
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Pasta {folder} criada. Adicione arquivos .md para fornecer contexto.")
        return combined

    # Iterar pelos arquivos na pasta
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    combined += f.read() + "\n\n"
            except Exception as e:
                print(f"Erro ao ler o arquivo {filename}: {e}")

    return combined
