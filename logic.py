# pylint: disable = "C0114, C0116, W0621, W0719, W0702, W0718, W0102, W0123, R0914, R0912"


def get_values(code, test_args=[10, 5]):
    values = {}
    param_dict = {}
    returns = []

    exec_stack = []  # pilha de blocos ativos: [{'indent': X, 'ativo': True/False}]
    i = 0

    while i < len(code):
        linha = code[i]["linha"]
        indent = code[i]["indent"]

        # Fecha blocos que terminaram
        while exec_stack and exec_stack[-1]["indent"] >= indent:
            exec_stack.pop()

        # Verifica se linha está em bloco ativo
        bloco_ativo = all(b["ativo"] for b in exec_stack)

        # 1. Definição da função
        if linha.startswith("def "):
            name_part = linha[4:].split("(")
            func_name = name_part[0]
            params = [
                p.strip() for p in name_part[1].split(")")[0].split(",") if p.strip()
            ]
            values[func_name] = params

            for idx, p in enumerate(params):
                val = str(test_args[idx]) if idx < len(test_args) else None
                values[p] = ["param"]
                if val is not None:
                    values[p].append(val)
                    param_dict[p] = val
            i += 1
            continue

        # 2. if / elif / else
        if linha.startswith(("if ", "elif ", "else")):
            tipo = linha.split()[0]
            indent_bloco = indent

            # só processa se estiver em bloco ativo
            if not bloco_ativo:
                i += 1
                continue

            if tipo == "else":
                cond = "True"
            else:
                cond = linha.split(" ", 1)[1].rstrip(":")
                for k, v in param_dict.items():
                    cond = cond.replace(k, v)
            try:
                resultado = eval(cond)
            except:
                resultado = False

            # Marca se esse bloco é ativo ou não
            exec_stack.append({"indent": indent_bloco, "ativo": resultado})
            i += 1
            continue

        # 3. Dentro de bloco ativo: atribuição
        if bloco_ativo and "=" in linha and "==" not in linha:
            var, expr = map(str.strip, linha.split("=", 1))
            expr_eval = expr
            for k, v in param_dict.items():
                expr_eval = expr_eval.replace(k, v)
            try:
                res = eval(expr_eval)
            except:
                res = None
            values[var] = [expr, res]
            if res is not None:
                param_dict[var] = str(res)

        # 4. Dentro de bloco ativo: return
        elif bloco_ativo and linha.startswith("return"):
            retorno = linha[len("return") :].strip()
            retorno_eval = retorno
            for k, v in param_dict.items():
                retorno_eval = retorno_eval.replace(k, v)
            try:
                res = eval(retorno_eval)
            except:
                res = None
            returns.append([retorno, res, True])
            values["returns"] = returns
            return values  # <- função termina aqui

        i += 1

    # fallback (caso múltiplos returns)
    for r in returns[:-1]:
        r[2] = False

    values["returns"] = returns
    return values


def bd_values(data):
    result = {}

    # 1. Nome da função
    func_name = next(
        (
            k
            for k, v in data.items()
            if isinstance(v, list)
            and k != "returns"
            and all(isinstance(x, str) for x in v)
        ),
        None,
    )

    # 2. Parâmetros de entrada
    params = data.get(func_name, []) if func_name else []
    result["qtde_param_entrada"] = len(params)
    result["valores_param_entrada"] = [
        data[p][1] for p in params if p in data and len(data[p]) > 1
    ]

    # 3. Variáveis internas (não são parâmetros nem returns)
    internas = [
        k for k in data if k not in [func_name, "returns"] and "param" not in data[k][0]
    ]
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


def vvar(tupla):
    """
    Aplica a fórmula V(Var) = soma de entradas + internas + saídas
    Espera tupla no formato:
    (id, qtd_entrada, '["val1", "val2"]', qtd_internas, '[val]', qtd_saida, '[val]')
    """

    def str_para_lista_floats(texto):
        texto = texto.strip().replace("[", "").replace("]", "")
        if not texto:
            return []
        return [
            float(x.strip().replace('"', "").replace("'", ""))
            for x in texto.split(",")
            if x.strip()
        ]

    entradas = str_para_lista_floats(tupla[2])
    internas = str_para_lista_floats(tupla[4])
    retornos = str_para_lista_floats(tupla[6])

    return sum(entradas) + sum(internas) + sum(retornos)
