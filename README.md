## 🧪 MTUS – 4º Equação (Vvar)

Este projeto é uma aplicação desktop com interface gráfica (GUI) feita com `tkinter`, que permite ao usuário comparar dois trechos de código Python (original e modificado), utilizando entradas de teste e salvando os resultados de análise em um banco de dados SQLite. Os códigos são analisados quanto às suas variáveis de entrada, intermediárias e saída.

### 🖼️ Interface

A interface gráfica possui dois campos para código (original e modificado), um campo para entrada de teste e botões para gerar a análise ou limpar os campos. O resultado da análise aparece em um pop-up.


### 📁 Estrutura de Pastas

```
├── main.py # Arquivo principal com a interface tkinter
├── modules/
│ ├── reader.py # Função que interpreta código a partir de texto
│ ├── logic.py # Executa o código, coleta variáveis, compara execuções
│ └── bd_conn.py # Criação de tabelas, inserções e consultas no SQLite
├── examples/
│ ├── code1.txt # Exemplo de código original
│ └── code2.txt # Exemplo de código modificado
└── MTUS.db # Banco de dados SQLite (gerado automaticamente após rodar a 1ª vez)
```

### 🧠 Como Funciona

#### 1. Entrada de Códigos
Você insere dois trechos de código Python (original e modificado) na interface. Esses códigos devem conter uma função principal com parâmetros.

#### 2. Entrada de Teste
Você informa os valores de entrada (ex: `10, 5`), que serão passados como argumentos para ambos os códigos.

#### 3. Execução e Registro
O programa executa ambos os códigos com as entradas fornecidas e coleta:
- Entradas (`e_t`)
- Variáveis intermediárias (`v_g`)
- Saídas (`s_h`)

#### 4. Salvamento no Banco
Os dados são salvos em:
- `analises`: armazena o resultado de cada execução
- `comparacoes`: registra o resultado da comparação entre os dois códigos

#### 5. Comparação (`vvar`)
As análises são comparadas usando a função `vvar()` e o resultado ("Igual" ou "Diferente") é exibido.


### 🧪 Exemplo de Uso

1. Cole dois códigos no formato:

```python
def somar(a, b):
    x = a + b
    return x
```
2. No campo de entrada, insira valores no formato: 10, 5 (sempre separe os valores de entrada por vírgula)

3. Clique em Gerar Análise.

4. Um pop-up mostrará os valores processados e se os dois códigos se comportam de forma igual ou não.

### 🗃️ Banco de Dados

O banco SQLite MTUS.db é criado automaticamente. Contém duas tabelas:

- analises:
    Armazena o nome da função, entradas, variáveis intermediárias e saídas.

- comparacoes: 
    Armazena o resultado da comparação entre duas análises.

### ▶️ Executando o Projeto

1. Certifique-se de ter Python instalado. Depois, execute:

```bash
python main.py
```

2. 🛠️ Requisitos

    - Python 3.8+

    - Bibliotecas nativas: tkinter, sqlite3, json

### 📌 Observações Técnicas

- O projeto utiliza eval() para simular a execução de código, então cuidado com código malicioso.

- Algumas flags do pylint estão desativadas por causa da natureza dinâmica do projeto (como uso de eval, exec, etc).

- Cada execução gera uma nova linha nas tabelas do banco.

### 📚 Créditos

Desenvolvido por Bruno Santos e Vítor Coutinho.