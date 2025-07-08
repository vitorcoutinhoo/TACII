# pylint: disable = "C0114, C0116, W0621, W0719, W0702, W0718, W0102, W0123, R0914, R0912"

import tkinter as tk
from tkinter import Toplevel, messagebox

from reader import reader
from logic import get_values, bd_values, vvar
from bd_conn import (
    criar_tabela_analises,
    criar_tabela_comparacoes,
    salvar_bd_values_analises,
    salvar_bd_values_comparacoes,
    listar_analises,
)


# -------------------------------------------------
# Função do Pop-up com resultados
# -------------------------------------------------
def show_popup(result1, result2, text):
    popup = Toplevel(root)
    popup.title("Resultados da Análise")
    popup.geometry("400x200")

    frame = tk.Frame(popup)
    frame.pack(pady=10, fill="both", expand=True)

    tk.Label(frame, text="RESULTADO VVAR ORIGINAL").pack()
    res1 = tk.Text(frame, height=1, wrap="word")
    res1.insert("1.0", result1)
    res1.config(state="disabled")
    res1.pack(fill="x", padx=10)

    tk.Label(frame, text="RESULTADO VVAR MODIFICADO").pack()
    res2 = tk.Text(frame, height=1, wrap="word")
    res2.insert("1.0", result2)
    res2.config(state="disabled")
    res2.pack(fill="x", padx=10)

    tk.Label(frame, text="ANÁLISE:").pack()
    res_text = tk.Text(frame, height=1, wrap="word")
    res_text.insert("1.0", text)
    res_text.config(state="disabled")
    res_text.pack(fill="x", padx=10)

    tk.Button(
        popup, text="Fechar", bg="#ff6666", fg="white", command=popup.destroy
    ).pack(pady=10)


# -------------------------------------------------
# Função principal da lógica
# -------------------------------------------------
def generate_result():
    entrada_usuario = entry_input.get().strip()

    if not entrada_usuario:
        messagebox.showwarning(
            "Entrada obrigatória", "Por favor, preencha o campo de entrada."
        )
        return

    try:
        case_test = [
            int(valor.strip()) for valor in entrada_usuario.split(",") if valor.strip()
        ]
        if not case_test:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Entrada inválida",
            "Insira apenas números inteiros separados por vírgulas.\nEx: 10, 5, 3",
        )
        return

    text1 = input1.get("1.0", tk.END).strip()
    text2 = input2.get("1.0", tk.END).strip()

    criar_tabela_analises()
    criar_tabela_comparacoes()

    t1 = reader(text1)
    t2 = reader(text2)

    result1 = bd_values(get_values(t1, case_test))
    result2 = bd_values(get_values(t2, case_test))

    salvar_bd_values_analises(result1)
    salvar_bd_values_analises(result2)

    analises = listar_analises()[:2]
    analise1, analise2 = analises[1], analises[0]

    v1 = vvar(analise1)
    v2 = vvar(analise2)

    txt = "Igual" if v1 == v2 else "Diferente"
    dados = {
        "id_analise1": analise1[0],
        "id_analise2": analise2[0],
        "resultado": txt,
    }
    salvar_bd_values_comparacoes(dados)

    show_popup(v1, v2, txt)


def clear_fields():
    input1.delete("1.0", tk.END)
    input2.delete("1.0", tk.END)
    entry_input.delete(0, tk.END)


# -------------------------------------------------
# Interface principal
# -------------------------------------------------
root = tk.Tk()
root.geometry("1100x500")
root.title("MTUS - Teste de Unidade de Software")

# Frame principal dividido em inputs e botões
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

code_frame = tk.Frame(main_frame)
code_frame.grid(row=0, column=0, sticky="nsew")

button_frame = tk.Frame(main_frame)
button_frame.grid(row=0, column=1, padx=20, sticky="n")

# Labels acima dos inputs
tk.Label(code_frame, text="Código Original").grid(row=0, column=0, pady=(0, 2))
tk.Label(code_frame, text="Código Modificado").grid(row=0, column=1, pady=(0, 2))

# Inputs de código
input1 = tk.Text(code_frame, width=50, height=28, relief="solid", bd=1)
input2 = tk.Text(code_frame, width=50, height=28, relief="solid", bd=1)
input1.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="nsew")
input2.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="nsew")

# Label para o input extra
tk.Label(button_frame, text="Digite a Entrada:").pack(pady=(10, 0))

# Input extra pequeno
entry_input = tk.Entry(button_frame, width=30, relief="solid", highlightthickness=1)
entry_input.pack(pady=(5, 10))

# Botões
tk.Button(
    button_frame,
    text="Gerar Análise",
    bg="#28a745",
    fg="white",
    width=30,
    command=generate_result,
).pack(pady=(15, 5))
tk.Button(
    button_frame,
    text="Limpar Inputs",
    bg="#ffc107",
    fg="black",
    width=30,
    command=clear_fields,
).pack(pady=2)

root.mainloop()
