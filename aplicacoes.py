import tkinter as tk
from tkinter import ttk

from plot import plotar_bode
from filtros import (filtro_passa_baixas, filtro_passa_altas, filtro_passa_faixa,
                     filtro_rejeita_faixa, filtro_passa_baixas_rl, filtro_passa_altas_rl)

def parse_valor(valor_str):
    valor_str = valor_str.lower().replace(" ", "").replace("ω", "").replace("f", "").replace("h", "")
    multiplicador = 1
    if 'k' in valor_str:
        multiplicador = 1e3
        valor_str = valor_str.replace('k', '')
    elif 'm' in valor_str:
        multiplicador = 1e-3
        valor_str = valor_str.replace('m', '')
    elif 'µ' in valor_str or 'u' in valor_str:
        multiplicador = 1e-6
        valor_str = valor_str.replace('µ', '').replace('u', '')
    elif 'n' in valor_str:
        multiplicador = 1e-9
        valor_str = valor_str.replace('n', '')
    elif 'p' in valor_str:
        multiplicador = 1e-12
        valor_str = valor_str.replace('p', '')

    return float(valor_str) * multiplicador

def mostrar_aplicacoes_reais(root, ajustar_tamanho_janela, mostrar_tela_inicial):
    # Limpa o conteúdo atual da janela
    for widget in root.winfo_children():
        widget.destroy()

    # Ajusta o tamanho da janela para a tela de aplicações reais
    ajustar_tamanho_janela(750, 750)

    # Frame para centralizar o conteúdo
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Adiciona o título
    ttk.Label(frame, text="Algumas Aplicações Reais", font=("Arial", 16, "bold")).pack(pady=20)

    # Adiciona os filtros e seus botões
    def criar_secao_filtro(titulo, botoes):
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=10, fill="x")

        # Título do filtro (centralizado)
        ttk.Label(sub_frame, text=titulo, font=("Arial", 14)).pack(anchor="center", pady=5)

        # Frame para centralizar os botões
        botoes_frame = ttk.Frame(sub_frame)
        botoes_frame.pack(anchor="center", pady=5)

        # Botões do filtro
        for botao_texto, botao_comando in botoes:
            ttk.Button(botoes_frame, text=botao_texto, command=botao_comando).pack(side="left", padx=2, pady=5)

    # Adiciona as seções de filtros
    criar_secao_filtro(
        "Filtro Passa-Baixa (RC)",
        [
            ("Crossover para Subwoofer", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Crossover para Subwoofer",
                "Subwoofers são alto-falantes projetados para reproduzir sons graves. Um filtro passa-baixas garante que apenas as frequências graves cheguem até ele.",
                {"R": "8 Ω", "C": "200 µF"}
            )),
            ("Suavização de Fonte de Alimentação", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Suavização de Fonte de Alimentação",
                "Um filtro passa-baixas remove a ondulação ('ripple') da corrente contínua, deixando passar apenas o sinal DC puro.",
                {"R": "15 Ω", "C": "1000 µF"}
            )),
            ("Controle de Tonalidade em Guitarras", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Controle de Tonalidade em Guitarras",
                "O botão de 'Tone' em uma guitarra elétrica é um filtro passa-baixas que ajusta o brilho do som.",
                {"R": "250 kΩ", "C": "47 nF"}
            )),
        ],
    )

    criar_secao_filtro(
        "Filtro Passa-Baixa (RL)",
        [
            ("Filtro de Ruído em Áudio", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Filtro de Ruído em Áudio",
                "Um filtro passa-baixas RL pode ser usado para remover ruídos de alta frequência (chiados) de linhas de áudio.",
                {"R": "100 Ω", "L": "10 mH"}
            )),
            ("Crossover Simples para Woofer", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Crossover Simples para Woofer",
                "Em sistemas de som mais simples, um indutor (filtro RL) pode ser usado para desviar as altas frequências do woofer.",
                {"R": "4 Ω", "L": "1 mH"}
            )),
            ("Suavização em Motores DC", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Suavização em Motores DC",
                "Um filtro RL pode suavizar a corrente fornecida a um motor DC, reduzindo o ruído elétrico e o desgaste.",
                {"R": "2 Ω", "L": "5 mH"}
            )),
        ],
    )

    criar_secao_filtro(
        "Filtro Passa-Alta (RC)",
        [
            ("Crossover para Tweeter", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Crossover para Tweeter",
                "Tweeters são alto-falantes feitos para sons agudos. Um filtro passa-altas bloqueia os graves e envia apenas os agudos para o tweeter.",
                {"R": "8 Ω", "C": "6.8 µF"}
            )),
            ("Capacitor de Acoplamento", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Capacitor de Acoplamento",
                "Um capacitor age como um filtro passa-altas que bloqueia a tensão DC e deixa o sinal de áudio AC passar.",
                {"R": "10 kΩ", "C": "1 µF"}
            )),
            ("Filtro 'Rumble' para Toca-discos", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Filtro 'Rumble' para Toca-discos",
                "Remove ruídos de baixa frequência causados pela vibração do motor do toca-discos.",
                {"R": "47 kΩ", "C": "150 nF"}
            )),
        ],
    )

    criar_secao_filtro(
        "Filtro Passa-Alta (RL)",
        [
            ("Diferenciador de Sinais", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Diferenciador de Sinais",
                "Um circuito RL passa-altas pode ser usado como um diferenciador para sinais de alta frequência.",
                {"R": "1 kΩ", "L": "100 mH"}
            )),
             ("'Presence Boost' em Amplificadores", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "'Presence Boost' em Amplificadores",
                "Em amplificadores de guitarra, um filtro RL passa-altas pode ser usado para dar um brilho extra nas frequências mais altas.",
                {"R": "10 kΩ", "L": "2 H"}
            )),
            ("Filtro para Linha de Transmissão", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Filtro para Linha de Transmissão",
                "Pode ser usado para bloquear correntes DC indesejadas em linhas de transmissão de sinais de alta frequência.",
                {"R": "50 Ω", "L": "500 mH"}
            )),
        ],
    )

    criar_secao_filtro(
        "Filtro Passa-Faixa",
        [
            ("Sintonizador de Rádio AM/FM", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Sintonizador de Rádio AM/FM",
                "O sintonizador do rádio é um filtro passa-faixa que deixa passar apenas a estação desejada.",
                {"R": "10 Ω", "L": "100 µH", "C": "250 pF"}
            )),
            ("Equalizador Gráfico de Áudio", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Equalizador Gráfico de Áudio",
                "Cada controle deslizante de um equalizador é um filtro passa-faixa que ajusta uma banda específica de frequências.",
                {"R": "1 kΩ", "L": "120 mH", "C": "33 nF"}
            )),
            ("Pedal de Wah-Wah para Guitarra", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Pedal de Wah-Wah para Guitarra",
                "O famoso efeito 'wah-wah' é um filtro passa-faixa onde a frequência central é varrida para cima e para baixo.",
                {"R": "1.5 kΩ", "L": "500 mH", "C": "82 nF"}
            )),
        ],
    )

    criar_secao_filtro(
        "Filtro Rejeita-Faixa",
        [
            ("Remoção de Ruído de Rede Elétrica", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Remoção de Ruído de Rede Elétrica",
                "Um filtro rejeita-faixa remove o zumbido constante de 60 Hz da rede elétrica.",
                {"R": "4 kΩ", "L": "1 H", "C": "7 µF"}
            )),
            ("Filtro DSL para Linha Telefônica", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Filtro DSL para Linha Telefônica",
                "Um filtro rejeita-faixa bloqueia as altas frequências usadas pela internet DSL, deixando passar apenas a voz.",
                {"R": "100 Ω", "L": "1 mH", "C": "2.5 nF"}
            )),
            ("Eliminador de Microfonia", lambda: mostrar_aplicacao(
                root, ajustar_tamanho_janela, mostrar_tela_inicial,
                "Eliminador de Microfonia",
                "Um filtro rejeita-faixa elimina a frequência específica da microfonia sem prejudicar o resto do som.",
                {"R": "82 kΩ", "L": "150 mH", "C": "10 nF"}
            )),
        ],
    )

    # Botão para voltar à tela inicial
    ttk.Button(frame, text="Voltar", command=mostrar_tela_inicial).pack(pady=5)

def mostrar_aplicacao(root, ajustar_tamanho_janela, mostrar_tela_inicial, titulo, explicacao, valores):
    # Limpa o conteúdo atual da janela
    for widget in root.winfo_children():
        widget.destroy()

    # Ajusta o tamanho da janela para a tela de aplicação
    ajustar_tamanho_janela(600, 400)

    # Frame para centralizar o conteúdo
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Adiciona o título
    ttk.Label(frame, text=titulo, font=("Arial", 16, "bold")).pack(pady=20)

    # Adiciona a explicação (com largura máxima para não ultrapassar as bordas)
    explicacao_label = ttk.Label(frame, text=explicacao, font=("Arial", 12), justify="center", wraplength=550)
    explicacao_label.pack(pady=10)

    # Adiciona os valores da aplicação
    valores_texto = "\n".join([f"{key}: {value}" for key, value in valores.items()])
    ttk.Label(frame, text=f"Valores de Exemplo:\n{valores_texto}", font=("Arial", 12), justify="center").pack(pady=10)

    # Botão para simular
    def simular():
        try:
            # Converte os valores do dicionário para números
            R_num = parse_valor(valores.get("R", "0"))
            C_num = parse_valor(valores.get("C", "0"))
            L_num = parse_valor(valores.get("L", "0"))

            # Determina qual filtro usar e plota o gráfico
            if "Passa-Baixa (RC)" in titulo or "Subwoofer" in titulo or "Fonte" in titulo or "Tonalidade" in titulo:
                system, freqs = filtro_passa_baixas(R_num, C_num)
                plotar_bode(system, titulo, freqs)
            
            elif "Passa-Baixa (RL)" in titulo or "Filtro de Ruído" in titulo or "Crossover Simples" in titulo or "Suavização em Motores" in titulo:
                system, freqs = filtro_passa_baixas_rl(R_num, L_num)
                plotar_bode(system, titulo, freqs)

            elif "Passa-Alta (RC)" in titulo or "Tweeter" in titulo or "Acoplamento" in titulo or "Rumble" in titulo:
                system, freqs = filtro_passa_altas(R_num, C_num)
                plotar_bode(system, titulo, freqs)
            
            elif "Passa-Alta (RL)" in titulo or "Diferenciador" in titulo or "Presence Boost" in titulo or "Linha de Transmissão" in titulo:
                system, freqs = filtro_passa_altas_rl(R_num, L_num)
                plotar_bode(system, titulo, freqs)

            elif "Passa-Faixa" in titulo or "Sintonizador" in titulo or "Equalizador" in titulo or "Wah-Wah" in titulo:
                system, freqs = filtro_passa_faixa(R_num, L_num, C_num)
                plotar_bode(system, titulo, freqs)

            elif "Rejeita-Faixa" in titulo or "Ruído" in titulo or "DSL" in titulo or "Microfonia" in titulo:
                system, freqs = filtro_rejeita_faixa(R_num, L_num, C_num)
                plotar_bode(system, titulo, freqs)

        except Exception as e:
            print(f"Erro ao simular: {e}")
            # (Opcional) Mostrar uma janela de erro para o usuário

    ttk.Button(frame, text="Simular", command=simular).pack(pady=15)

    # Botão para voltar à tela de aplicações reais
    ttk.Button(frame, text="Voltar", command=lambda: mostrar_aplicacoes_reais(root, ajustar_tamanho_janela, mostrar_tela_inicial)).pack(pady=5)