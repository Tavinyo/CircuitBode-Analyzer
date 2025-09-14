import tkinter as tk
from tkinter import ttk

from aplicacoes import mostrar_aplicacoes_reais
from interfaces import mostrar_filtro_personalizado, mostrar_sobre

def criar_interface():
    def centralizar_janela(janela, largura, altura):
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x = (screen_width - largura) // 2
        y = (screen_height - altura) // 2
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def ajustar_tamanho_janela(largura, altura):
        centralizar_janela(root, largura, altura)

    def mostrar_tela_inicial():
        for widget in root.winfo_children():
            widget.destroy()

        ajustar_tamanho_janela(400, 300)

        ttk.Label(root, text="Simulador de Filtros", font=("Arial", 16, "bold")).pack(pady=20)

        # Botões que chamam as funções importadas
        ttk.Button(root, text="Aplicações Reais", command=lambda: mostrar_aplicacoes_reais(root, ajustar_tamanho_janela, mostrar_tela_inicial)).pack(pady=20)
        ttk.Button(root, text="Filtro Personalizado", command=lambda: mostrar_filtro_personalizado(root, ajustar_tamanho_janela, centralizar_janela, mostrar_tela_inicial)).pack(pady=20)
        ttk.Button(root, text="Fechar", command=root.destroy).pack(pady=20)
        
        sobre_btn = ttk.Button(root, text="Sobre", command=lambda: mostrar_sobre(root, ajustar_tamanho_janela, mostrar_tela_inicial))
        sobre_btn.place(relx=0.95, rely=0.95, anchor="se")

    # Criação da janela principal
    root = tk.Tk()
    root.title("Simulação de Filtros")
    root.resizable(False, False)
    
    # Exibe a tela inicial
    mostrar_tela_inicial()

    root.mainloop()

# --- Bloco Principal ---
if __name__ == '__main__':
    criar_interface()