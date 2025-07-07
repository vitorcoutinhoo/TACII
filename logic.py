# pylint: disable = "C0114, C0116, W0621, W0719, W0702, W0102, W0123, R0914, R0912"

from reader import reader

def get_values(code, test_args=[10, 5]):
    values = {}
    param_dict = {}
    returns = []                     # <- NOVO: acumula cada return

    for line in code:
        line = line.strip()

        # Ignorar blocos de controle e comentários
        if line.startswith(("if", "for", "while", "else", "elif", "#")):
            continue

        # 1. Definição da função
        if line.startswith("def "):
            name_part = line[4:].split("(")
            func_name = name_part[0]
            params = [p.strip() for p in name_part[1].split(")")[0].split(",") if p.strip()]
            values[func_name] = params

            for i, p in enumerate(params):
                val = str(test_args[i]) if i < len(test_args) else None
                values[p] = ['param']
                if val is not None:
                    values[p].append(val)
                    param_dict[p] = val  # salva valor como string

        # 2. Retorno – agora acumulamos
        elif line.startswith("return"):
            returned = line[len("return"):].strip()
            entry = [returned]       # primeiro item: expressão textual

            # tentar calcular o valor retornado
            if returned in values and len(values[returned]) == 2:
                entry.append(values[returned][1])
            else:
                expr_eval = returned
                for k, v in param_dict.items():
                    expr_eval = expr_eval.replace(k, v)
                try:
                    entry.append(eval(expr_eval))
                except Exception:
                    pass            # mantém só a expressão se não der pra avaliar

            returns.append(entry)    # guarda este return

        # 3. Atribuições (suporta múltiplas separadas por vírgula)
        elif "=" in line:
            parts = line.split(",")
            for part in parts:
                if "=" in part:
                    var, expr = map(str.strip, part.split("=", 1))
                    expr_eval = expr
                    for k, v in param_dict.items():
                        expr_eval = expr_eval.replace(k, v)
                    try:
                        result = eval(expr_eval)
                    except Exception:
                        result = None
                    values[var] = [expr, result]
                    if result is not None:
                        param_dict[var] = str(result)

    values["returns"] = returns      # <- guarda lista completa de returns
    return values


def bd_values(data):
    result = {}

    # 1. Nome da função
    func_name = next(
        (k for k, v in data.items()
         if isinstance(v, list) and k != "returns" and all(isinstance(x, str) for x in v)),
        None)

    # 2. Parâmetros de entrada
    params = data.get(func_name, []) if func_name else []
    result["qtde_param_entrada"] = len(params)
    result["valores_param_entrada"] = [
        data[p][1] for p in params if p in data and len(data[p]) > 1
    ]

    # 3. Variáveis internas (não são parâmetros nem returns)
    internas = [k for k in data
                if k not in [func_name, "returns"] and 'param' not in data[k][0]]
    result["qtde_variaveis_internas"] = len(internas)
    result["valores_variaveis_internas"] = [
        data[k][1] for k in internas if len(data[k]) > 1
    ]

    # 4. Variáveis retornadas
    returns = data.get("returns", [])
    result["qtde_variaveis_retorno"] = len(returns)
    result["valores_retorno"] = [
        r[1] for r in returns if len(r) > 1
    ]  # só pega se conseguimos calcular

    return result


# Exemplo rápido
if __name__ == "__main__":
    codigo = reader("code.txt")      # seu arquivo de teste
    print(bd_values(get_values(codigo)))
