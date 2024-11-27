import random
import time
import os

def clear_screen():
    # Limpa a tela para dar o efeito de atualização rápida no terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Lista inicial de 10 animais
    animais = [
        "Elefante", "Tigre", "Girafa", "Leão", "Urso", 
        "Rinoceronte", "Panda", "Lobo", "Canguru", "Zebra"
    ]

    print("Pressione Enter para selecionar um animal aleatório!")
    print("Você fará 5 seleções.")

    # Número de seleções desejadas
    selecoes = 5

    for _ in range(selecoes):
        # Aguarda o usuário apertar Enter para iniciar a seleção
        input("\nPressione Enter para escolher um animal...")

        # Animação para mostrar os animais mudando rapidamente
        for _ in range(10):  # Loop para o efeito de rotação dos animais
            clear_screen()
            print("Selecionando...")
            print(random.choice(animais))  # Exibe um animal aleatório da lista
            time.sleep(0.1)  # Espera brevemente antes de trocar o animal

        # Seleciona o animal final e remove-o da lista
        escolhido = random.choice(animais)
        animais.remove(escolhido)
        clear_screen()
        print(f"Animal selecionado: {escolhido}")

    print("\nFim do jogo! Os animais selecionados foram removidos da lista.")
