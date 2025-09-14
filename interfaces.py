import tkinter as tk
from tkinter import ttk

from filtros import filtro_passa_baixas, filtro_passa_altas, filtro_passa_faixa, filtro_rejeita_faixa, filtro_passa_baixas_rl, filtro_passa_altas_rl
from plot import plotar_bode

def mostrar_filtro_personalizado(root, ajustar_tamanho_janela, centralizar_janela, mostrar_tela_inicial):
    # Limpa o conteúdo atual da janela
    for widget in root.winfo_children():
        widget.destroy()

    # Ajusta o tamanho da janela para a tela de filtro personalizado
    ajustar_tamanho_janela(400, 400)

    # Frame para centralizar o conteúdo
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Dropdown para selecionar o tipo de filtro
    filtro_var = tk.StringVar(value="Passa-Baixas (RC)")
    ttk.Label(frame, text="Tipo de Filtro:").grid(row=0, column=0, padx=10, pady=10)
    filtro_dropdown = ttk.Combobox(frame, textvariable=filtro_var,
                                   values=["Passa-Baixas (RC)", "Passa-Altas (RC)", "Passa-Baixas (RL)", "Passa-Altas (RL)", "Passa-Faixa", "Rejeita-Faixa"],
                                   state="readonly")
    filtro_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Entradas para R, L e C
    ttk.Label(frame, text="Resistência (R):").grid(row=1, column=0, padx=10, pady=10)
    entry_R = ttk.Entry(frame)
    entry_R.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Indutância (L):").grid(row=2, column=0, padx=10, pady=10)
    entry_L = ttk.Entry(frame, state="disabled")  # Inicialmente desabilitado
    entry_L.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Capacitância (C):").grid(row=3, column=0, padx=10, pady=10)
    entry_C = ttk.Entry(frame)
    entry_C.grid(row=3, column=1, padx=10, pady=10)

    # Atualiza o estado dos campos de entrada
    def atualizar_campos(*args):
        filtro_selecionado = filtro_var.get()
        if filtro_selecionado in ["Passa-Baixas (RC)", "Passa-Altas (RC)"]:
            entry_L.config(state="disabled")
            entry_C.config(state="normal")
        elif filtro_selecionado in ["Passa-Baixas (RL)", "Passa-Altas (RL)"]:
            entry_L.config(state="normal")
            entry_C.config(state="disabled")
        else:
            entry_L.config(state="normal")
            entry_C.config(state="normal")

    filtro_var.trace_add("write", atualizar_campos)
    atualizar_campos() # Chamada inicial

    # Botão para calcular e plotar
    def calcular():
        tipo_filtro = filtro_var.get()
        try:
            R = float(entry_R.get())
            if tipo_filtro in ["Passa-Baixas (RC)", "Passa-Altas (RC)", "Passa-Faixa", "Rejeita-Faixa"]:
                C = float(entry_C.get())
            else:
                C = None
            if tipo_filtro in ["Passa-Baixas (RL)", "Passa-Altas (RL)", "Passa-Faixa", "Rejeita-Faixa"]:
                L = float(entry_L.get())
            else:
                L = None


            # Validação de entradas
            if R <= 0 or (C is not None and C <= 0) or (L is not None and L <= 0):
                raise ValueError("Os valores de R, L e C devem ser positivos.")

            if tipo_filtro == 'Passa-Baixas (RC)':
                system, freqs = filtro_passa_baixas(R, C)
                titulo = f"Filtro Passa-Baixas (R={R}, C={C})"
            elif tipo_filtro == 'Passa-Altas (RC)':
                system, freqs = filtro_passa_altas(R, C)
                titulo = f"Filtro Passa-Altas (R={R}, C={C})"
            elif tipo_filtro == 'Passa-Baixas (RL)':
                system, freqs = filtro_passa_baixas_rl(R, L)
                titulo = f"Filtro Passa-Baixas (R={R}, L={L})"
            elif tipo_filtro == 'Passa-Altas (RL)':
                system, freqs = filtro_passa_altas_rl(R, L)
                titulo = f"Filtro Passa-Altas (R={R}, L={L})"
            elif tipo_filtro == 'Passa-Faixa':
                system, freqs = filtro_passa_faixa(R, L, C)
                titulo = f"Filtro Passa-Faixa (R={R}, L={L}, C={C})"
            elif tipo_filtro == 'Rejeita-Faixa':
                system, freqs = filtro_rejeita_faixa(R, L, C)
                titulo = f"Filtro Rejeita-Faixa (R={R}, L={L}, C={C})"
            else:
                return

            # Plota o gráfico
            plotar_bode(system, titulo, freqs=freqs)
        except ValueError as e:
            # Abre uma janela de erro
            error_window = tk.Toplevel(root)
            error_window.title("Erro")
            ttk.Label(error_window, text=str(e)).pack(padx=20, pady=20)
            ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
            centralizar_janela(error_window, 300, 150)

    calcular_btn = ttk.Button(frame, text="Calcular", command=calcular)
    calcular_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # Botão para voltar à tela inicial
    ttk.Button(root, text="Voltar", command=mostrar_tela_inicial).pack(pady=10)

def mostrar_sobre(root, ajustar_tamanho_janela, mostrar_tela_inicial):
    # Limpa o conteúdo atual da janela
    for widget in root.winfo_children():
        widget.destroy()

    ajustar_tamanho_janela(600, 300)

    texto_sobre = (
        "Projeto de Eletricidade II:\n"
        "Simulador de Filtros de Primeira e Segunda Ordem\n\n"
        "Professor:\n"
        "Luciano Sales Barros\n\n"
        "Grupo:\n"
        "Gustavo Antônio Sales Estevão\n"
        "Marina Donza Fernandes Correa\n"
        "Antônio Justino de Araújo Filho\n"
        "Alessandra Cardoso Fernandes"
    )
    ttk.Label(root, text=texto_sobre, font=("Arial", 12), justify="center").pack(padx=20, pady=20)
    ttk.Button(root, text="Voltar", command=mostrar_tela_inicial).pack(pady=10)