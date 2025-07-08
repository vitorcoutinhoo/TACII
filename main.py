import tkinter as tk
import logic
import reader
from pprint import pformat

# -------------------------------------------------
# Funções de interface
# -------------------------------------------------
def generate_result():
    """Lê os dois códigos digitados, processa e mostra os resultados."""
    text1 = input1.get("1.0", tk.END).strip()
    text2 = input2.get("1.0", tk.END).strip()

    # Converte para estrutura esperada pelo logic
    t1 = reader.reader(text1)
    t2 = reader.reader(text2)

    result1 = pformat(logic.bd_values(logic.get_values(t1, [10, 5])))
    result2 = pformat(logic.bd_values(logic.get_values(t2, [10, 5])))

    # --- escreve no output1 ---
    output1.config(state="normal")        # habilita
    output1.delete("1.0", tk.END)
    output1.insert(tk.END, result1)
    output1.config(state="disabled")      # desabilita novamente

    # --- escreve no output2 ---
    output2.config(state="normal")
    output2.delete("1.0", tk.END)
    output2.insert(tk.END, result2)
    output2.config(state="disabled")

def clear_fields():
    """Limpa todos os campos e restaura o estado desabilitado dos outputs."""
    input1.delete("1.0", tk.END)
    input2.delete("1.0", tk.END)

    output1.config(state="normal")
    output1.delete("1.0", tk.END)
    output1.config(state="disabled")

    output2.config(state="normal")
    output2.delete("1.0", tk.END)
    output2.config(state="disabled")

# -------------------------------------------------
# Janela principal
# -------------------------------------------------
root = tk.Tk()
root.geometry("900x600")
root.title("MTUS - Teste de Unidade de Software")

# -------------------------------------------------
# Frames de layout (linha de cima = entradas / linha de baixo = saídas)
# -------------------------------------------------
top_frame    = tk.Frame(root)
bottom_frame = tk.Frame(root)
btn_frame    = tk.Frame(root)

top_frame.grid(row=0, column=0, sticky="nsew")
bottom_frame.grid(row=1, column=0, sticky="nsew")
btn_frame.grid(row=2, column=0, pady=10)

# Faz as linhas crescerem ao redimensionar
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Cada frame (superior e inferior) terá duas colunas expansíveis
for f in (top_frame, bottom_frame):
    f.columnconfigure(0, weight=1)
    f.columnconfigure(1, weight=1)
    f.rowconfigure(0, weight=1)

# -------------------------------------------------
# Widgets
# -------------------------------------------------
# Entradas
input1 = tk.Text(top_frame, wrap="word")
input2 = tk.Text(top_frame, wrap="word")
input1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
input2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Saídas (começam desabilitadas)
output1 = tk.Text(bottom_frame, wrap="word", bg="#e0e0e0", state="disabled")
output2 = tk.Text(bottom_frame, wrap="word", bg="#e0e0e0", state="disabled")
output1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
output2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Botões
run_btn   = tk.Button(btn_frame, text="Gerar Resultado", command=generate_result)
clear_btn = tk.Button(btn_frame, text="Apagar Campos",   command=clear_fields)
run_btn.pack(side="left",  padx=10)
clear_btn.pack(side="left", padx=10)

# -------------------------------------------------
# Loop principal
# -------------------------------------------------
root.mainloop()
