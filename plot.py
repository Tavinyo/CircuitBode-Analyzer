import numpy as np
import matplotlib.pyplot as plt

def plotar_bode(system, title, freqs=None):
    """
    Plota o Diagrama de Bode (Magnitude e Fase) para um dado sistema.
    """
    w_range = np.logspace(0, 6, 1000)
    w_calc, mag_db, phase = system.bode(w_range)
    
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
    
    if freqs:
        # Pega a primeira frequência para definir um range inicial razoável
        first_freq = next(iter(freqs.values()))
        freq_min = first_freq / 10
        freq_max = first_freq * 10
        
        # Ajusta o range se houver múltiplas frequências
        freq_values = [v for k, v in freqs.items() if k.lower() != 'q']
        if freq_values:
            freq_min = min(freq_values) / 10
            freq_max = max(freq_values) * 10

        ax1.set_xlim(freq_min, freq_max)
        ax2.set_xlim(freq_min, freq_max)

    legend_labels = []
    param_labels = []
    if freqs:
        for key, val in freqs.items():
            if key.lower() == 'q':
                param_labels.append(f"Fator Q = {val:.2f}")
            else:
                ax1.axvline(x=val, color='r', linestyle='--')
                ax2.axvline(x=val, color='r', linestyle='--')
                
                y_marker_magnitude = np.interp(val, w_calc, ganho_linear)
                y_marker_phase = np.interp(val, w_calc, phase)
                ax1.plot(val, y_marker_magnitude, 'ro')
                ax2.plot(val, y_marker_phase, 'ro')
                
                legend_labels.append(f"{key} = {val:.2f} rad/s")
                ax1.text(val * 1.05, y_marker_magnitude, f'{key}', color='r', ha='left')
    
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.text(1.05, -0.02, 'ω', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')
        if ax == ax1:
            ax.text(-0.02, 1.05, '|H(jω)|', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')
        else:
            ax.text(-0.02, 1.05, 'Fase', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black')

    if legend_labels or param_labels:
        # Junta as legendas de frequência e de parâmetros
        full_legend_list = legend_labels + param_labels
        legend_text = "   |   ".join(full_legend_list)
        fig.text(0.5, 0.03, legend_text, ha='center', fontsize=10, color='black',
                 bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='square,pad=0.3'))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()