# pylint: disable = "C0114, C0116, W0621, W0719, W0702, W0718, W0102, W0123, R0914, R0912"

from reader import reader
from logic import get_values, bd_values, vvar
from bd_conn import (
    criar_tabela_analises,
    criar_tabela_comparacoes,
    salvar_bd_values_analises,
    salvar_bd_values_comparacoes,
    listar_analises,
    listar_comparacoes
)

# Cria as tabelas no banco de dados
criar_tabela_analises()
criar_tabela_comparacoes()

# Lê os códigos
codigo1 = reader("code1.txt")
codigo2 = reader("code2.txt")

# Executa os códigos com os mesmos testes
case_test = [4, 3]
teste1 = get_values(codigo1, case_test)
teste2 = get_values(codigo2, case_test)

# Converte os dados para o formato de salvamento
values1 = bd_values(teste1)
values2 = bd_values(teste2)

# Salva no banco
salvar_bd_values_analises(values1)
salvar_bd_values_analises(values2)

# Recupera os dois últimos registros (já ordenados por ID decrescente)
analises = listar_analises()[:2]  # Pega os 2 últimos registros
analise1, analise2 = analises[1], analises[0]  # Inverter pois estão em ordem DESC

# Calcula V(Var)
v1 = vvar(analise1)
v2 = vvar(analise2)

# Prepara e salva a comparação
dados = {
    "id_analise1": analise1[0],
    "id_analise2": analise2[0],
    "resultado": "Igual" if v1 == v2 else "Diferente"
}

salvar_bd_values_comparacoes(dados)

for analise in listar_analises():
    print(analise)

print("--------------------------------")

for comparacao in listar_comparacoes():
    print(comparacao)
