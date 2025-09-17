import numpy as np
from scipy.signal import TransferFunction

def filtro_passa_baixas(R, C, wc):
    if wc is None and R is not None and C is not None:
        wc = 1 / (R * C)
    freqs = {'wc': wc}

    if R is None and wc is not None and C is not None:
        R = 1 / (wc * C)
    if C is None and wc is not None and R is not None:
        C = 1 / (wc * R)

    num = [1]
    den = [R * C, 1]
    print(f"Filtro Passa-Baixas com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs, R, C, wc

def filtro_passa_altas(R, C, wc):
    if wc is None and R is not None and C is not None:
        wc = 1 / (R * C)
    freqs = {'wc': wc}

    if R is None and wc is not None and C is not None:
        R = 1 / (wc * C)
    if C is None and wc is not None and R is not None:
        C = 1 / (wc * R)

    num = [R * C, 0]
    den = [R * C, 1]
    print(f"Filtro Passa-Altas com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs, R, C, wc

def filtro_passa_baixas_rl(R, L, wc):
    print(R, L, wc)
    if wc is None and R is not None and L is not None:
        wc = R / L
    elif R is None and L is not None and wc is not None:
        R = wc * L
    elif L is None and R is not None and wc is not None:
        L = R / wc
    else:
        raise ValueError("Forneça pelo menos dois dos valores (R, L, Wc).")

    freqs = {'wc': wc}
    num = [R/L]
    den = [1, R/L]
    print(f"Filtro Passa-Baixas RL com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs, R, L, wc

def filtro_passa_altas_rl(R, L, wc):
    if wc is None and R is not None and L is not None:
        wc = R / L
    freqs = {'wc': wc}

    if R is None and L is not None and wc is not None:
        R = wc * L
    if L is None and R is not None and wc is not None:
        L = R / wc

    num = [1, 0]
    den = [1, R/L]
    print(f"Filtro Passa-Altas RL com wc = {wc:.2f} rad/s")
    return TransferFunction(num, den), freqs, R, L, wc

def filtro_passa_faixa(R, L, C, Q, wc1, wc2):
    if Q is not None and (R is not None or C is not None or L is not None) and (wc1 is not None and wc2 is not None):
        #Fornecido Q, faixa de banda, e algum componente
        w0 = np.sqrt(wc1 * wc2)
        bw = w0 / Q

        if R is not None:
            L = R / bw
            C = 1 / (L * w0 * w0)
        elif C is not None:
            L = 1 / (C * w0 * w0)
            R = L * bw
        elif L is not None:
            R = L * bw
            C = 1 / (L * w0 * w0)
        else:
            raise ValueError("Forneça o fator Q e pelo menos um componente (R, L ou C).")
        
    elif R is not None and L is not None and C is not None:
        #R, L ou C fornecidos
        w0 = 1 / np.sqrt(L * C)
        bw = R / L
        Q = w0 / bw
        wc1 = w0 / (2 * Q) * (np.sqrt(1 + (2 * Q)**2) - 1)
        wc2 = w0 / (2 * Q) * (np.sqrt(1 + (2 * Q)**2) + 1)

    elif wc1 is not None and wc2 is not None and (R is not None or L is not None or C is not None):
        #Faixa de banda e um dos componentes fornecidos
        w0 = np.sqrt(wc1 * wc2)
        bw = wc2 - wc1
        Q = w0 / bw
        
        if R is not None:
            L = R / bw
            C = 1 / (L * w0**2)
        elif L is not None:
            R = L * bw
            C = 1 / (L * w0**2)
        elif C is not None:
            L = 1 / (C * w0**2)
            R = L * bw

    if None in [R, L, C]:
        raise ValueError("Não foi possível determinar todos os parâmetros. "
                         "Forneça pelo menos dois entre (R, L, C) ou (wc1, wc2).")

    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2, 'Q': Q}
    num = [R/L, 0]
    den = [1, R/L, 1/(L*C)]

    print(f"Filtro Passa-Faixa com w0 = {w0:.2f} rad/s")
    return TransferFunction(num, den), freqs_plot, R, L, C, wc1, wc2

def filtro_rejeita_faixa(R, L, C, Q, wc1, wc2):
    if Q is not None and (R is not None or C is not None or L is not None) and (wc1 is not None and wc2 is not None):
        #Fornecido Q, faixa de banda, e algum componente
        w0 = np.sqrt(wc1 * wc2)
        bw = w0 / Q

        if R is not None:
            L = R / bw
            C = 1 / (L * w0 * w0)
        elif C is not None:
            L = 1 / (C * w0 * w0)
            R = L * bw
        elif L is not None:
            R = L * bw
            C = 1 / (L * w0 * w0)
        else:
            raise ValueError("Forneça o fator Q e pelo menos um componente (R, L ou C).")
        
    elif R is not None and L is not None and C is not None:
        #R, L ou C fornecidos
        w0 = 1 / np.sqrt(L * C)
        bw = R / L
        Q = w0 / bw
        wc1 = w0 / (2 * Q) * (np.sqrt(1 + (2 * Q)**2) - 1)
        wc2 = w0 / (2 * Q) * (np.sqrt(1 + (2 * Q)**2) + 1)

    elif wc1 is not None and wc2 is not None and (R is not None or L is not None or C is not None):
        #Faixa de banda e um dos componentes fornecidos
        w0 = np.sqrt(wc1 * wc2)
        bw = wc2 - wc1
        Q = w0 / bw
        
        if R is not None:
            L = R / bw
            C = 1 / (L * w0**2)
        elif L is not None:
            R = L * bw
            C = 1 / (L * w0**2)
        elif C is not None:
            L = 1 / (C * w0**2)
            R = L * bw

    if None in [R, L, C]:
        raise ValueError("Não foi possível determinar todos os parâmetros. "
                         "Forneça pelo menos dois entre (R, L, C) ou (wc1, wc2).")

    freqs_plot = {'w0': w0, 'wc1': wc1, 'wc2': wc2, 'Q': Q}
    num = [1, 0, 1/(L*C)]
    den = [1, R/L, 1/(L*C)]
    print(f"Filtro Rejeita-Faixa com w0 de rejeicao = {w0:.2f} rad/s")
    return TransferFunction(num, den), freqs_plot, R, L, C, wc1, wc2