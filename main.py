import tkinter as tk

# Função chamada quando o botão for clicado
def generate_result():
    # Pega o texto dos campos de entrada
    text1 = input1.get("1.0", tk.END).strip()
    text2 = input2.get("1.0", tk.END).strip()

    print("Texto 1:", text1)
    print("Texto 2:", text2)

    # Simula um processamento (aqui só transforma em maiúsculas)
    result1 = text1.upper()
    result2 = text2.upper()

    # Coloca o texto processado nos campos de saída
    output1.delete("1.0", tk.END)
    output1.insert(tk.END, result1)

    output2.delete("1.0", tk.END)
    output2.insert(tk.END, result2)

def clear_fields():
    input1.delete("1.0", tk.END)
    input2.delete("1.0", tk.END)
    output1.delete("1.0", tk.END)
    output2.delete("1.0", tk.END)

# Cria a janela principal
root = tk.Tk()
root.title("Processador de Texto")
root.geometry("800x600")

# Campo de entrada 1
input1 = tk.Text(root, height=5)
input1.pack(pady=5, fill=tk.X)

# Campo de entrada 2
input2 = tk.Text(root, height=5)
input2.pack(pady=5, fill=tk.X)

# Botão Gerar Resultado
result_button = tk.Button(root, text="Gerar Resultado", command=generate_result)
result_button.pack(pady=10)

# Botão Apagar Campos
result_button = tk.Button(root, text="Apagar Campos", command=clear_fields)
result_button.pack(pady=10)

# Campo de saída 1
output1 = tk.Text(root, height=5, bg="#e0e0e0")
output1.pack(pady=5, fill=tk.X)

# Campo de saída 2
output2 = tk.Text(root, height=5, bg="#e0e0e0")
output2.pack(pady=5, fill=tk.X)

# Inicia a interface
root.mainloop()
