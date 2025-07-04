# pylint: disable = "C0114, C0116, W0621, W0719"


def reader(path):
    """
    Função que lê o arquivo de código e destaca as
    palavras reservadas e operadores.

    param:
        path: Caminho do arquivo de código.
    return:
        Código formatado e separado por linhas com destaque 
        para palavras reservadas e operadores.
        
    """
    res = None
    with open(path, "r", encoding="utf-8") as file:
        codigo = file.read()
    res = codigo.replace(" ", "")

    # destaca as palavras reservadas
    for symbol in ["def", "if", "else", "elif", "for", "while", "return"]:
        res = res.replace(symbol, f"{symbol} ")

    # destaca os operadores
    for symbol in ["=", "<=", ">=", "==", "and", "or", "not", "is"]:
        res = res.replace(symbol, f" {symbol} ")

    # Separa as linhas
    lines = []
    for line in res.split("\n"):
        lines.append(line)
    return lines
