import numpy as np
from scipy.signal import TransferFunction

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

def filtro_passa_baixas_rl(R, L):
    wc = R / L
    freqs = {'wc': wc}
    num = [R/L]
    den = [1, R/L]
    print(f"Filtro Passa-Baixas RL com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs

def filtro_passa_altas_rl(R, L):
    wc = R / L
    freqs = {'wc': wc}
    num = [1, 0]
    den = [1, R/L]
    print(f"Filtro Passa-Altas RL com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs

def filtro_passa_faixa(R, L, C):
    w0 = 1 / np.sqrt(L * C)
    bw = R / L
    q_factor = w0 / bw
    wc1 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) - 1/(2*q_factor))
    wc2 = w0 * (np.sqrt(1 + (1/(2*q_factor))**2) + 1/(2*q_factor))
    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2, 'Q': q_factor}
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
    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2, 'Q': q_factor}
    num = [1, 0, 1/(L*C)]
    den = [1, R/L, 1/(L*C)]
    print(f"Filtro Rejeita-Faixa com w0 de rejeicao = {w0:.2f} rad/s")
    return TransferFunction(num, den), freqs_plot