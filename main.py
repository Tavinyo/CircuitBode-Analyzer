import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode

def plotar_bode(system, title, freqs=None):

    # Usamos uma faixa de w diretamente, de 1 rad/s a 1M rad/s
    w_range = np.logspace(0, 6, 1000)

    w_calc, mag_db, phase = bode(system, w_range)
    
    ganho_linear = 10**(mag_db / 20)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(title, fontsize=16)

    # Plot do Ganho
    ax1.semilogx(w_calc, ganho_linear)
    ax1.grid(which='both', linestyle='--')
    ax1.set_title('Diagrama de Magnitude')

    # Plot da Fase
    ax2.semilogx(w_calc, phase)
    ax2.grid(which='both', linestyle='--')
    ax2.set_title('Diagrama de Fase')
    
    # --- Ajusta os limites do eixo X ---
    if freqs:
        # Determina os limites do eixo X com base nas frequências características
        freq_min = min(freqs.values()) / 10  # Uma década abaixo da menor frequência característica
        freq_max = max(freqs.values()) * 10  # Uma década acima da maior frequência característica
        ax1.set_xlim(freq_min, freq_max)
        ax2.set_xlim(freq_min, freq_max)

    # --- Adiciona as marcacoes no grafico ---
    legend_labels = []  # Lista para armazenar os rótulos das frequências
    if freqs:
        for key, w_val in freqs.items():
            # Desenha a linha vertical em ambos os graficos
            ax1.axvline(x=w_val, color='r', linestyle='--')
            ax2.axvline(x=w_val, color='r', linestyle='--')
            
            # Adiciona um ponto no gráfico de magnitude
            y_marker_magnitude = np.interp(w_val, w_calc, ganho_linear)
            y_marker_phase = np.interp(w_val, w_calc, phase)
            ax1.plot(w_val, y_marker_magnitude, 'ro')  # 'ro' = red o (círculo vermelho)
            ax2.plot(w_val, y_marker_phase, 'ro')  # 'ro' = red o (círculo vermelho)
            
            # Adiciona os valores das interseções no lado direito do gráfico (opcional, pra conferir que o cáculo está correto)
            ax1.text(freq_max * 0.9, y_marker_magnitude, f"{key}: {y_marker_magnitude:.2f}", color='r', ha='left')
            ax2.text(freq_max * 0.9, y_marker_phase, f"{key}: {y_marker_phase:.2f}", color='r', ha='left')
        
            # Adiciona a frequência na legenda
            legend_labels.append(f"{key} = {w_val:.2f} rad/s")
            
            # Adiciona o nome da frequência ao lado do ponto
            ax1.text(w_val * 1.05, y_marker_magnitude, f'{key}', color='r', ha='left')
    
    # --- Personalizando os eixos ---
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if ax == ax1:
            ax.text(1.05, -0.02, 'ω', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')
            ax.text(-0.02, 1.05, '|H(jω)|', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')
        elif ax == ax2:
            ax.text(1.05, -0.02, 'ω', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')
            ax.text(-0.02, 1.05, 'Fase', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')


    # Adiciona os valores das frequências abaixo do gráfico
    if legend_labels:
        legend_text = "   |   ".join(legend_labels)  # Junta os valores lado a lado com separadores
        fig.text(0.5, 0.03, legend_text, ha='center', fontsize=10, color='black',
                 bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='square,pad=0.3'))


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- Filtros ---

def filtro_passa_baixas(R, C):
    wc = 1 / (R * C)
    freqs = {'wc': wc}
    num = [1]
    den = [R * C, 1]
    print(f"Filtro Passa-Baixas com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs

def filtro_passa_altas(R, C):
    wc = 1 / (R * C)
    freqs = {'wc': wc}
    num = [R * C, 0]
    den = [R * C, 1]
    print(f"Filtro Passa-Altas com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs

def filtro_passa_faixa(R, L, C):
    w0 = 1 / np.sqrt(L * C)
    bw = R / L
    q_factor = w0 / bw
    wc1 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) - 1/(2*q_factor))
    wc2 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) + 1/(2*q_factor))
    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2}
    num = [R/L, 0]
    den = [1, R/L, 1/(L*C)]
    print(f"Filtro Passa-Faixa com w0 = {w0:.2f} rad/s")
    return TransferFunction(num, den), freqs_plot

def filtro_rejeita_faixa(R, L, C):
    w0 = 1 / np.sqrt(L * C)
    bw = R / L
    q_factor = w0 / bw
    wc1 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) - 1/(2*q_factor))
    wc2 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) + 1/(2*q_factor))
    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2}
    num = [1, 0, 1/(L*C)]
    den = [1, R/L, 1/(L*C)]
    print(f"Filtro Rejeita-Faixa com w0 de rejeicao = {w0:.2f} rad/s")
    return TransferFunction(num, den), freqs_plot

# --- Processamento de arquivo ---
def processar_arquivo_de_filtros(nome_arquivo):
    print(f"Lendo filtros do arquivo: {nome_arquivo}\n")
    try:
        with open(nome_arquivo, 'r') as f:
            for i, linha in enumerate(f):
                linha_limpa = linha.strip()
                if not linha_limpa or linha_limpa.startswith('#'):
                    continue

                partes = [p.strip() for p in linha_limpa.split(',')]
                tipo_filtro = partes[0].lower()
                
                try:
                    valores = [float(v) for v in partes[1:]]
                    filtro_system, freqs = None, None
                    titulo = ""

                    if tipo_filtro == 'passa-baixas' and len(valores) == 2:
                        R, C = valores
                        filtro_system, freqs = filtro_passa_baixas(R, C)
                        titulo = f"Filtro Passa-Baixas (R={R} Ohm, C={C} F)"
                    
                    elif tipo_filtro == 'passa-altas' and len(valores) == 2:
                        R, C = valores
                        filtro_system, freqs = filtro_passa_altas(R, C)
                        titulo = f"Filtro Passa-Altas (R={R} Ohm, C={C} F)"

                    elif tipo_filtro == 'passa-faixa' and len(valores) == 3:
                        R, L, C = valores
                        filtro_system, freqs = filtro_passa_faixa(R, L, C)
                        titulo = f"Filtro Passa-Faixa (R={R}, L={L}, C={C})"
                    
                    elif tipo_filtro == 'rejeita-faixa' and len(valores) == 3:
                        R, L, C = valores
                        filtro_system, freqs = filtro_rejeita_faixa(R, L, C)
                        titulo = f"Filtro Rejeita-Faixa (R={R}, L={L}, C={C})"

                    else:
                        print(f"AVISO: Linha {i+1}: Formato desconhecido ou numero incorreto de parametros para '{tipo_filtro}'.")
                        continue

                    if filtro_system:
                        # Passamos o dicionario de frequencias para a funcao de plotagem
                        plotar_bode(filtro_system, titulo, freqs=freqs)

                except ValueError:
                    print(f"AVISO: Linha {i+1}: Nao foi possivel converter os valores para numeros. Pulando linha.")
                except IndexError:
                    print(f"AVISO: Linha {i+1}: Faltam parametros. Pulando linha.")

    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada '{nome_arquivo}' nao encontrado.")
        print("Por favor, crie o arquivo com os filtros que deseja simular.")

# --- Bloco Principal de Execucao (inlaterado) ---
if __name__ == '__main__':
    nome_do_arquivo_de_entrada = 'filtros.txt'
    processar_arquivo_de_filtros(nome_do_arquivo_de_entrada)
    print("\nSimulacao concluida.")