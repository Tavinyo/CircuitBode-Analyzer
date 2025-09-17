import tkinter as tk
from tkinter import ttk

from filtros import filtro_passa_baixas, filtro_passa_altas, filtro_passa_faixa, filtro_rejeita_faixa, filtro_passa_baixas_rl, filtro_passa_altas_rl
from plot import plotar_bode

def mostrar_filtro_personalizado(root, ajustar_tamanho_janela, centralizar_janela, mostrar_tela_inicial):
    # Limpa o conteúdo atual da janela
    for widget in root.winfo_children():
        widget.destroy()

    # Ajusta o tamanho da janela para a tela de filtro personalizado
    ajustar_tamanho_janela(800, 600)

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

    # Entradas
    ttk.Label(frame, text="Resistência (R):").grid(row=1, column=0, padx=10, pady=10)
    entry_R = ttk.Entry(frame)
    entry_R.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Indutância (L):").grid(row=2, column=0, padx=10, pady=10)
    entry_L = ttk.Entry(frame, state="disabled")  # Inicialmente desabilitado
    entry_L.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Capacitância (C):").grid(row=3, column=0, padx=10, pady=10)
    entry_C = ttk.Entry(frame)
    entry_C.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Frequência de Corte (Wc):").grid(row=4, column=0, padx=10, pady=10)
    entry_Wc = ttk.Entry(frame)
    entry_Wc.grid(row=4, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Fator Q:").grid(row=5, column=0, padx=10, pady=10)
    entry_Q = ttk.Entry(frame)
    entry_Q.grid(row=5, column=1, padx=10, pady=10)
    
    ttk.Label(frame, text="Banda de Passagem/Rejeição (Wc1 | Wc2):").grid(row=6, column=0, padx=10, pady=10)
    entry_Wc1 = ttk.Entry(frame)
    entry_Wc1.grid(row=6, column=1, padx=10, pady=10)
    entry_Wc2 = ttk.Entry(frame)
    entry_Wc2.grid(row=6, column=2, padx=10, pady=10)

    entries = [entry_R, entry_L, entry_C, entry_Wc, entry_Wc1, entry_Wc2, entry_Q]
    listaRC = [entry_R, entry_C, entry_Wc]
    listaRL = [entry_R, entry_L, entry_Wc]
    listaRLC = [entry_R, entry_C, entry_L, entry_Wc1, entry_Wc2, entry_Q]

    # Atualiza o estado dos campos de entrada
    def atualizar_campos(*args):
        # Calcula quantos campos foram preenchidos
        preenchidos = [e for e in entries if e.get().strip() != ""]
        n = len(preenchidos)
        filtro_selecionado = filtro_var.get()

        if filtro_selecionado in ["Passa-Baixas (RC)", "Passa-Altas (RC)"]:
            preenchidosRC = [e for e in listaRC if e.get().strip() != ""]
        
            for m in entries:
                if m not in listaRC:
                    m.config(state="normal")
                    m.delete(0, tk.END)
                    m.config(state="disable")
                else:
                    m.config(state="normal")

            if len(preenchidosRC) >= 2:
                for m in entries:
                    if m.get().strip() != "" and m in listaRC:
                        m.config(state="normal")
                    elif m.get().strip() == "" and m in listaRC:
                        m.config(state="disable")

        elif filtro_selecionado in ["Passa-Baixas (RL)", "Passa-Altas (RL)"]:
            preenchidosRL = [e for e in listaRL if e.get().strip() != ""]
        
            for m in entries:
                if m not in listaRL:
                    m.config(state="normal")
                    m.delete(0, tk.END)
                    m.config(state="disable")
                else:
                    m.config(state="normal")

            if len(preenchidosRL) >= 2:
                for m in entries:
                    if m.get().strip() != "" and m in listaRL:
                        m.config(state="normal")
                    elif m.get().strip() == "" and m in listaRL:
                        m.config(state="disable")

        elif filtro_selecionado in ["Passa-Faixa", "Rejeita-Faixa"]:
            preenchidosRLC = [e for e in listaRLC if e.get().strip() != ""]
            n = len(preenchidosRLC)
        
            for m in entries:
                if m not in listaRLC:
                    m.config(state="normal")
                    m.delete(0, tk.END)
                    m.config(state="disable")
                else:
                    m.config(state="normal")

            #Fixa em 3 caso tenha sido passado uma faixa e um componente
            if(entry_Wc1.get().strip() != "" or entry_Wc2.get().strip() != "") and (entry_R.get().strip() != "" or entry_C.get().strip() != "" or entry_L.get().strip() != ""):
                n = 3
            
            #Fixa o n em dois caso tenha fornecido uma faixa e o Q, pois só poderá escolher mais um componente
            if (entry_Wc1.get().strip() != "" or entry_Wc2.get().strip() != "") and (entry_Q.get().strip() != ""):
                if (entry_R.get().strip() != "" or entry_C.get().strip() != "" or entry_L.get().strip() != ""):
                    n = 3
                else:
                    n = 2

            #Fixa o n em 3 caso R, L e C tenham sido fornecidos
            if (entry_R.get().strip() != "" and entry_C.get().strip() != "" and entry_L.get().strip() != ""):
                n = 3

            print(n)
                
            if n >= 3:
                for m in entries:
                    if m.get().strip() != "" and m in listaRLC:
                        m.config(state="normal")
                    elif m.get().strip() == "" and m in listaRLC:
                        m.config(state="disable")

            if (entry_R.get().strip() != "" and entry_L.get().strip() != "" and entry_C.get().strip() != ""):
                entry_Wc1.config(state="disabled")
                entry_Wc2.config(state="disabled")
            else:
                entry_Wc1.config(state="normal")
                entry_Wc2.config(state="normal")

    #Configuração de reatividade da interface
    filtro_var.trace_add("write", atualizar_campos)
    entry_R.bind("<KeyRelease>", atualizar_campos)
    entry_L.bind("<KeyRelease>", atualizar_campos)
    entry_C.bind("<KeyRelease>", atualizar_campos)
    entry_Wc.bind("<KeyRelease>", atualizar_campos)
    entry_Wc1.bind("<KeyRelease>", atualizar_campos)
    entry_Wc2.bind("<KeyRelease>", atualizar_campos)
    entry_Q.bind("<KeyRelease>", atualizar_campos)
    atualizar_campos() # Chamada inicial

    def formatar(valor):
        if valor == None:
            return ""

        elif abs(valor) <= 1e-2 or abs(valor) > 1e3:
            return f"{valor:.2e}"
        
        else:
            return f"{valor:.2f}"

    # Botão para calcular e plotar
    def calcular():
        tipo_filtro = filtro_var.get()
        try:
            R = float(entry_R.get()) if entry_R.get().strip() else None
            L = float(entry_L.get()) if entry_L.get().strip() else None
            C = float(entry_C.get()) if entry_C.get().strip() else None
            Wc = float(entry_Wc.get()) if entry_Wc.get().strip() else None
            Wc1 = float(entry_Wc1.get()) if entry_Wc1.get().strip() else None
            Wc2 = float(entry_Wc2.get()) if entry_Wc2.get().strip() else None
            Q = float(entry_Q.get()) if entry_Q.get().strip() else None


            # Validação de entradas
            if (R is not None and R <= 0) or (C is not None and C <= 0) or (L is not None and L <= 0) or (Wc is not None and Wc <= 0) or (Wc1 is not None and Wc1 <= 0) or (Wc2 is not None and Wc2 <= 0) or (Q is not None and Q <= 0):
                raise ValueError("Os valores devem ser positivos.")

            if tipo_filtro == 'Passa-Baixas (RC)':
                system, freqs, R, C, Wc = filtro_passa_baixas(R, C, Wc)
                titulo = f"Filtro Passa-Baixas (R={formatar(R)}, C={formatar(C)}, Wc={formatar(Wc)})"
            elif tipo_filtro == 'Passa-Altas (RC)':
                system, freqs, R, C, Wc = filtro_passa_altas(R, C, Wc)
                titulo = f"Filtro Passa-Altas (R={formatar(R)}, C={formatar(C)}, Wc={formatar(Wc)})"
            elif tipo_filtro == 'Passa-Baixas (RL)':
                system, freqs, R, L, Wc = filtro_passa_baixas_rl(R, L, Wc)
                titulo = f"Filtro Passa-Baixas (R={formatar(R)}, L={formatar(L)}, Wc={formatar(Wc)})"
            elif tipo_filtro == 'Passa-Altas (RL)':
                system, freqs, R, L, Wc = filtro_passa_altas_rl(R, L, Wc)
                titulo = f"Filtro Passa-Altas (R={formatar(R)}, L={formatar(L)}, Wc={formatar(Wc)})"
            elif tipo_filtro == 'Passa-Faixa':
                system, freqs, R, L, C, Wc1, Wc2 = filtro_passa_faixa(R, L, C, Q, Wc1, Wc2)
                titulo = f"Filtro Passa-Faixa (R={formatar(R)}, L={formatar(L)}, C={formatar(C)}, Wc1={formatar(Wc1)}, Wc2={formatar(Wc2)})"
            elif tipo_filtro == 'Rejeita-Faixa':
                system, freqs, R, L, C, Wc1, Wc2 = filtro_rejeita_faixa(R, L, C, Q, Wc1, Wc2)
                titulo = f"Filtro Rejeita-Faixa (R={formatar(R)}, L={formatar(L)}, C={formatar(C)}, Wc1={formatar(Wc1)}, Wc2={formatar(Wc2)})"
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


    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    calcular_btn = ttk.Button(frame, text="Calcular", command=calcular)
    calcular_btn.grid(row=7, column=0, columnspan=3, pady=20, sticky="n")

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