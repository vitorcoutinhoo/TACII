# pylint: disable = "C0114, C0116, W0621, W0719"

def reader(path):
    """
    Função que lê o arquivo de código e retorna as linhas originais.

    param:
        path: Caminho do arquivo de código.
    return:
        Lista de linhas do código (sem remover espaços ou formatar).
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.readlines()
