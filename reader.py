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
    res = codigo.replace(" ", "")

    # destaca as palavras reservadas
    for symbol in ["def", "if", "elif", "for", "while", "return"]:
        res = res.replace(symbol, f"{symbol} ")

    # destaca os operadores
    symbols = r'''(<=|>=|==|!=|=|\+|-|\*|/|%|//|\*\*|<|>|and|or|not)'''
    for symbol in re.findall(symbols, res):
        if symbol not in ["and", "or", "not"]:
            res = res.replace(symbol, f" {symbol} ")
        else:
            res = res.replace(symbol, f"{symbol} ")

    # Separa as linhas
    lines = []
    for line in res.split("\n"):
        lines.append(line)
    return lines
