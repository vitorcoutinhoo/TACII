# pylint: disable = "C0114, C0116, W0621, W0719"

import re

def reader(path):
    """
    Função que lê o arquivo de código e retorna as linhas originais.

    param:
        path: Caminho do arquivo de código.
    return:
        Lista de linhas do código (sem remover espaços ou formatar).
    """
    with open(path, "r", encoding="utf-8") as file:
        codigo = file.read()
    
    # Substitui tabulações por 4 espaços (padrão)
    codigo = codigo.replace("\t", "    ")

    # 1. Adiciona espaço após palavras-chave (com borda de palavra)
    for keyword in ["def", "if", "else", "elif", "for", "while", "return"]:
        codigo = re.sub(rf'\b{keyword}\b', f"{keyword} ", codigo)

    # 2. Adiciona espaço em volta dos operadores
    padrao_operadores = r'(<=|>=|==|!=|//|\*\*|<|>|=|\+|-|\*|/|%|\band\b|\bor\b|\bnot\b)'
    codigo = re.sub(padrao_operadores, r' \1 ', codigo)

    # 3. Quebra em linhas e limpa espaços duplicados por linha
    linhas = []
    for linha in codigo.splitlines():
        indent = len(linha) - len(linha.lstrip(" "))
        linha_limpa = re.sub(r'\s+', ' ', linha).strip()
        if linha_limpa:  # ignora linhas totalmente vazias
            linhas.append({
                "linha": linha_limpa,
                "indent": indent
            })

    return linhas
