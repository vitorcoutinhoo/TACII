# pylint: disable = "C0114, C0116, W0621, W0719, W0702, W0102, W0123, R0914, R0912"

from reader import reader

def get_values(code, test_args=[10, 5]):
    values = {}
    param_dict = {}

    for line in code:
        line = line.strip()

        # 1. Definição da função
        if line.startswith("def "):
            name_part = line[4:].split("(")
            func_name = name_part[0]
            params = name_part[1].split(")")[0].split(",")
            params = [p.strip() for p in params if p.strip()]
            values[func_name] = params

            for i, p in enumerate(params):
                val = str(test_args[i]) if test_args and i < len(test_args) else None
                values[p] = ['param']
                if val:
                    values[p].append(val)
                    param_dict[p] = val  # salva valor como string

        # 2. Retorno
        elif line.startswith("return"):
            returned = line[len("return"):].strip()
            values["return"] = [returned]

            # se o retorno for uma variável conhecida, tenta calcular seu valor
            if returned in values and len(values[returned]) == 2:
                values["return"].append(values[returned][1])
            else:
                # substitui e tenta calcular expressão
                try:
                    expr_eval = returned
                    for k, v in param_dict.items():
                        expr_eval = expr_eval.replace(k, v)
                    result = eval(expr_eval)
                    values["return"].append(result)
                except:
                    pass

        # 3. Atribuições com múltiplas expressões
        elif "=" in line:
            parts = line.split(",")
            for part in parts:
                if "=" in part:
                    var, expr = part.split("=", 1)
                    var = var.strip()
                    expr = expr.strip()

                    # expressão substituída para avaliar
                    expr_eval = expr
                    for k, v in param_dict.items():
                        expr_eval = expr_eval.replace(k, v)

                    try:
                        result = eval(expr_eval)
                    except:
                        result = None

                    values[var] = [expr, result]
                    if result is not None:
                        param_dict[var] = str(result)

    return values

def bd_values(data):
    result = {}

    # 1. Pega o nome da função (primeira chave que não é 'return' nem uma variável)
    func_name = next((k for k, v in data.items() if isinstance(v, list) and all(isinstance(x, str) for x in v)), None)

    # 2. Parâmetros de entrada
    params = data.get(func_name, []) if func_name else []
    result["qtde_param_entrada"] = len(params)
    result["valores_param_entrada"] = [data[p][1] for p in params if p in data and len(data[p]) > 1]

    # 3. Variáveis internas (tem valor calculado, mas não são 'return' nem parâmetros)
    variaveis_internas = [k for k in data if k not in [func_name, 'return'] and 'param' not in data[k][0]]
    result["qtde_variaveis_internas"] = len(variaveis_internas)
    result["valores_variaveis_internas"] = [data[k][1] for k in variaveis_internas if len(data[k]) > 1]

    # 4. Variáveis retornadas (valores dentro da chave 'return')
    if 'return' in data:
        retornadas = [r.strip() for r in data['return'][0].split(",")]
        result["qtde_variaveis_retorno"] = len(retornadas)

        # pega o valor(s) real(is) retornado(s)
        if len(data['return']) > 1:
            retorno_real = data['return'][1]
            # se for uma tupla/lista com múltiplos valores
            if isinstance(retorno_real, (tuple, list)):
                result["valores_retorno"] = list(retorno_real)
            else:
                result["valores_retorno"] = [retorno_real]
        else:
            result["valores_retorno"] = []

    return result

# print(get_values(reader("code.txt")))
print(bd_values(get_values(reader("code.txt"))))
