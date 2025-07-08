# pylint: disable = "C0114, C0116, W0621, W0719"

import sqlite3
import json

def conectar(nome_banco="MTUS.db"):
    """
    Conecta ao banco SQLite. Cria arquivo se não existir.
    """
    return sqlite3.connect(nome_banco)

def criar_tabela_analises():
    """
    Cria a tabela 'analises' se não existir.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qtde_param_entrada INTEGER,
            valores_param_entrada TEXT,
            qtde_variaveis_internas INTEGER,
            valores_variaveis_internas TEXT,
            qtde_variaveis_retorno INTEGER,
            valores_retorno TEXT
        )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_comparacoes():
    """
    Cria a tabela 'comparacoes' se não existir.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comparacoes (
            id_analise1 INTEGER,
            id_analise2 INTEGER,
            resultado TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_bd_values_analises(dados):
    """
    Insere um registro no banco com os dados do bd_values().
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO analises (
            qtde_param_entrada,
            valores_param_entrada,
            qtde_variaveis_internas,
            valores_variaveis_internas,
            qtde_variaveis_retorno,
            valores_retorno
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        dados['qtde_param_entrada'],
        json.dumps(dados['valores_param_entrada']),
        dados['qtde_variaveis_internas'],
        json.dumps(dados['valores_variaveis_internas']),
        dados['qtde_variaveis_retorno'],
        json.dumps(dados['valores_retorno']),
    ))
    conn.commit()
    conn.close()

def salvar_bd_values_comparacoes(dados):
    """
    Insere um registro no banco com os dados de comparações.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO comparacoes (id_analise1, id_analise2, resultado)
        VALUES (?, ?, ?)
    ''', (dados['id_analise1'], dados['id_analise2'], dados['resultado']))
    conn.commit()
    conn.close()

def listar_analises():
    """
    Retorna lista com todos registros da tabela 'analises'.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM analises ORDER BY id DESC")
    resultados = cur.fetchall()
    conn.close()
    return resultados

def listar_comparacoes():
    """
    Retorna lista com todos registros da tabela 'comparacoes'.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM comparacoes")
    resultados = cur.fetchall()
    conn.close()
    return resultados

def delete_analises():
    """
    Deleta todos os registros da tabela 'analises'.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM analises")
    conn.commit()
    conn.close()
