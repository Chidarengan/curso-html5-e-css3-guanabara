import tkinter as tk
 # from tkinter import messagebox

# Função para garantir que o usuário insira um número inteiro não negativo, vazio é considerado 0
def validar_numero(entrada):
    if entrada == "":
        return 0
    try:
        valor = int(entrada)
        if valor >= 0:
            return valor
        else:
            raise ValueError
    except ValueError:
        return None

# Função para validar a entrada de números no campo
def validar_caracteres(entrada):
    return entrada.isdigit() or entrada == ""  # Permite apenas números ou campo vazio


# Função que calcula a soma de uma progressão aritmética (PA)
def calcular_soma_progressao_aritmetica(a1, an):
    n = (an - a1) + 1  # Calcula o número de termos
    sn = (n * (a1 + an) // 2) - a1  # Calcula a soma dos termos da PA
    return sn


# Função para exibir a tabela "Dados e Modificador" com a nova coluna Mod/2
def exibir_dados_e_modificador(statuses):
    # Cabeçalho atualizado com a nova coluna Mod/2
    resultado = "Status          | Dado  |   Mod     | Mod/2  | Save  |\n"
    resultado += "------------------------------------------------------\n"


    for nome, valor in statuses.items():
        # Definindo o dado e o valor máximo conforme o status
        if valor <= 4:
            dado = "d4"
            total_dado = 4
        elif valor <= 6:
            dado = "d6"
            total_dado = 6
        elif valor <= 8:
            dado = "d8"
            total_dado = 8
        elif valor <= 10:
            dado = "d10"
            total_dado = 10
        elif valor <= 12:
            dado = "d12"
            total_dado = 12
        elif valor <= 50:
            dado = "d20"
            total_dado = 20
        elif valor <= 100:
            dado = "d50"
            total_dado = 50
        else:
            dado = "d100"
            total_dado = 100

        # Calculando modificadores e o Save
        modificador = valor // 2
        modificador_destreza = valor // 3 if nome == "Destreza" else None
        save = (total_dado * 40 // 100) + modificador  # Cálculo do Save
        mod_div2 = modificador // 2  # Novo valor para Mod/2

        # Centralizando os valores dentro das colunas, mantendo espaço suficiente para até 4 dígitos
        if nome == "Destreza":
            # Para destreza, exibir os dois modificadores separados por "/" e o Mod/2 normal
            resultado += f"{nome:<15} | {dado:^5} | {modificador:^4}/{modificador_destreza:^4} |  {mod_div2:^5} | {save:^5} |\n"
        else:
            # Para os outros status, exibir o modificador normal e Mod/2
            resultado += f"{nome:<15} | {dado:^5} | {modificador:^9} |  {mod_div2:^5} | {save:^5} |\n"

    return resultado


# Função para exibir os gastos de pontos por status de forma organizada e centralizada
def exibir_gastos_por_status(gastos):
    resultado = "Status          |  Gasto  |\n"
    resultado += "---------------------------\n"

    for nome, gasto in gastos.items():
        # Ajusta o alinhamento para que os valores fiquem centralizados na tabela
        resultado += f"{nome:<15} | {str(gasto):^7} |\n"

    return resultado

# Função para exibir o resultado em uma área de texto copiável com tamanho ajustável
def mostrar_resultado(titulo, resultado, altura_caixa=26, largura_caixa=55):
    limpar_janela()
    tk.Label(root, text=titulo, font=("Arial", 14)).pack(pady=10)

    # Área de texto para permitir copiar o resultado, tamanho ajustável por opção
    text_area = tk.Text(root, height=altura_caixa, width=largura_caixa, wrap="word")  # Ajustando o wrap para quebra por palavra
    text_area.pack(pady=10)

    # Inserindo o resultado no Text e tornando-o não editável
    text_area.insert(tk.END, resultado)
    text_area.config(state=tk.DISABLED)

    # Botão para voltar ao menu
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=20)

# Função para limpar o conteúdo atual da janela
def limpar_janela():
    for widget in root.winfo_children():
        widget.destroy()

# Função da opção 1: Total de Pontos Gastos e Outras Informações de Personagem
def opcao_1():
    try:
        forca = validar_numero(entry_forca.get())
        destreza = validar_numero(entry_destreza.get())
        agilidade = validar_numero(entry_agilidade.get())
        resistencia = validar_numero(entry_resistencia.get())
        inteligencia = validar_numero(entry_inteligencia.get())
        carisma = validar_numero(entry_carisma.get())

        if None in (forca, destreza, agilidade, resistencia, inteligencia, carisma):
            raise ValueError

        nivel = forca + destreza + agilidade + resistencia + inteligencia + carisma

        A = (resistencia // 10) * 0.3
        B = (nivel // 100) * 0.5
        X = A + B
        hp = int(nivel * (X + 1))

        gasto_forca = calcular_soma_progressao_aritmetica(0, forca)
        gasto_destreza = calcular_soma_progressao_aritmetica(0, destreza)
        gasto_agilidade = calcular_soma_progressao_aritmetica(0, agilidade)
        gasto_resistencia = calcular_soma_progressao_aritmetica(0, resistencia)
        gasto_inteligencia = calcular_soma_progressao_aritmetica(0, inteligencia)
        gasto_carisma = calcular_soma_progressao_aritmetica(0, carisma)

        gasto_total = (gasto_forca + gasto_destreza + gasto_agilidade +
                       gasto_resistencia + gasto_inteligencia + gasto_carisma)

        statuses = {
            "Força": forca,
            "Destreza": destreza,
            "Agilidade": agilidade,
            "Resistência": resistencia,
            "Inteligência": inteligencia,
            "Carisma": carisma
        }

        gastos_por_status = {
            "Força": gasto_forca,
            "Destreza": gasto_destreza,
            "Agilidade": gasto_agilidade,
            "Resistência": gasto_resistencia,
            "Inteligência": gasto_inteligencia,
            "Carisma": gasto_carisma
        }

        # Cálculo do Effort
        effort_d12 = nivel // 60
        effort_d20 = nivel // 100
        effort_d50 = nivel // 250

        resultado_effort = (f"Effort: {effort_d12}d12, {effort_d20}d20, {effort_d50}d50\n")

        tabela_status = exibir_dados_e_modificador(statuses)
        tabela_gastos = exibir_gastos_por_status(gastos_por_status)

        resultado = (f"Seu nível é: {nivel}\n"
                     f"Seus pontos de vida total são: {hp}\n\n"
                     f"Seu gasto de pontos em cada status foi:\n{tabela_gastos}\n"
                     f"Seu gasto total de pontos foi: {gasto_total}\n\n"
                     f"{resultado_effort}\n"  # Mostrando o effort
                     f"{tabela_status}")

        mostrar_resultado("Resultado", resultado, altura_caixa=26, largura_caixa=55)

    except ValueError:
        mostrar_resultado("Erro", "Por favor, insira valores válidos.", altura_caixa=10, largura_caixa=40)

# Função da opção 2: Cálculo Rápido de Pontos de Vida
def opcao_2():
    try:
        nivel = validar_numero(entry_nivel.get())
        resistencia = validar_numero(entry_resistencia_2.get())

        if nivel is None or resistencia is None or nivel < resistencia:
            raise ValueError

        A = (resistencia // 10) * 0.3
        B = (nivel // 100) * 0.5
        X = A + B
        hp = int(nivel * (X + 1))

        mostrar_resultado("Resultado", f"Seus pontos de vida total são: {hp}", altura_caixa=5, largura_caixa=40)

    except ValueError:
        mostrar_resultado("Erro", "Nível inválido ou entrada incorreta.", altura_caixa=5, largura_caixa=40)

# Função da opção 3: Gasto para Evolução de Status
def opcao_3():
    try:
        a1 = validar_numero(entry_a1.get())
        an = validar_numero(entry_an.get())

        if a1 is None or an is None or an <= a1:
            raise ValueError

        gasto = calcular_soma_progressao_aritmetica(a1, an)
        mostrar_resultado("Resultado", f"O total de pontos necessários para aumentar de {a1} até {an} é: {gasto} pontos", altura_caixa=5, largura_caixa=40)

    except ValueError:
        mostrar_resultado("Erro", "Valores inválidos. O valor final deve ser maior que o inicial.", altura_caixa=5, largura_caixa=40)


# Função para exibir a janela do menu principal com tamanho maior e centralizada
def mostrar_menu():
    limpar_janela()
    tk.Label(root, text="Saudações! O que você deseja?", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="1. Total de Pontos Gastos e Outras Informações de Personagem", command=abrir_opcao_1).pack(pady=5)
    tk.Button(root, text="2. Cálculo Rápido de Pontos de Vida", command=abrir_opcao_2).pack(pady=5)
    tk.Button(root, text="3. Gasto Para Evolução de Status", command=abrir_opcao_3).pack(pady=5)
    tk.Button(root, text="4. Distribuir Pontos em Tempo Real", command=abrir_opcao_4).pack(pady=5)  # Nova opção

# Funções para abrir cada opção na mesmo janela
def abrir_opcao_1():
    global entry_forca, entry_destreza, entry_agilidade, entry_resistencia, entry_inteligencia, entry_carisma
    limpar_janela()

    vcmd = root.register(validar_caracteres)  # Registro da função de validação

    tk.Label(root, text="Me diga sua Força atual:").pack(pady=5)
    entry_forca = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_forca.pack(pady=5)

    tk.Label(root, text="Me diga sua Destreza atual:").pack(pady=5)
    entry_destreza = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_destreza.pack(pady=5)

    tk.Label(root, text="Me diga sua Agilidade atual:").pack(pady=5)
    entry_agilidade = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_agilidade.pack(pady=5)

    tk.Label(root, text="Me diga sua Resistência atual:").pack(pady=5)
    entry_resistencia = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_resistencia.pack(pady=5)

    tk.Label(root, text="Me diga sua Inteligência atual:").pack(pady=5)
    entry_inteligencia = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_inteligencia.pack(pady=5)

    tk.Label(root, text="Me diga seu Carisma atual:").pack(pady=5)
    entry_carisma = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_carisma.pack(pady=5)

    tk.Button(root, text="Calcular", command=opcao_1).pack(pady=20)
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=5)

def abrir_opcao_2():
    global entry_nivel, entry_resistencia_2
    limpar_janela()

    vcmd = root.register(validar_caracteres)  # Registro da função de validação

    tk.Label(root, text="Me diga seu nível atual:").pack(pady=5)
    entry_nivel = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_nivel.pack(pady=5)

    tk.Label(root, text="Me diga sua resistência atual:").pack(pady=5)
    entry_resistencia_2 = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_resistencia_2.pack(pady=5)

    tk.Button(root, text="Calcular", command=opcao_2).pack(pady=20)
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=5)

def abrir_opcao_3():
    global entry_a1, entry_an
    limpar_janela()

    vcmd = root.register(validar_caracteres)  # Registro da função de validação

    tk.Label(root, text="Valor inicial:").pack(pady=5)
    entry_a1 = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_a1.pack(pady=5)

    tk.Label(root, text="Valor final:").pack(pady=5)
    entry_an = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_an.pack(pady=5)

    tk.Button(root, text="Calcular", command=opcao_3).pack(pady=20)
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=5)


# Função para exibir a janela do menu principal


# Função para a opção 4: Distribuição de Pontos em Tempo Real
def abrir_opcao_4():
    global entry_forca, entry_destreza, entry_agilidade, entry_resistencia, entry_inteligencia, entry_carisma, entry_pontos
    limpar_janela()

    vcmd = root.register(validar_caracteres)  # Registro da função de validação

    tk.Label(root, text="Digite Seus Status Atuais:", font=("Arial", 12)).pack(pady=5)

    tk.Label(root, text="Força:").pack(pady=5)
    entry_forca = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_forca.pack(pady=5)

    tk.Label(root, text="Destreza:").pack(pady=5)
    entry_destreza = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_destreza.pack(pady=5)

    tk.Label(root, text="Agilidade:").pack(pady=5)
    entry_agilidade = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_agilidade.pack(pady=5)

    tk.Label(root, text="Resistência:").pack(pady=5)
    entry_resistencia = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_resistencia.pack(pady=5)

    tk.Label(root, text="Inteligência:").pack(pady=5)
    entry_inteligencia = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_inteligencia.pack(pady=5)

    tk.Label(root, text="Carisma:").pack(pady=5)
    entry_carisma = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_carisma.pack(pady=5)

    tk.Label(root, text="Pontos Para Distribuir:").pack(pady=5)
    entry_pontos = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry_pontos.pack(pady=5)

    tk.Button(root, text="Calcular", command=distribuir_pontos).pack(pady=20)
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=5)

# Função para a distribuição de pontos em tempo real
def distribuir_pontos():
    global pontos_disponiveis, status_atual, botoes_status

    # Validar entradas de status e pontos disponíveis
    try:
        forca = validar_numero(entry_forca.get())
        destreza = validar_numero(entry_destreza.get())
        agilidade = validar_numero(entry_agilidade.get())
        resistencia = validar_numero(entry_resistencia.get())
        inteligencia = validar_numero(entry_inteligencia.get())
        carisma = validar_numero(entry_carisma.get())
        pontos_disponiveis = validar_numero(entry_pontos.get())

        if None in (forca, destreza, agilidade, resistencia, inteligencia, carisma, pontos_disponiveis):
            raise ValueError

        status_atual = {
            "Força": forca,
            "Destreza": destreza,
            "Agilidade": agilidade,
            "Resistência": resistencia,
            "Inteligência": inteligencia,
            "Carisma": carisma
        }

        botoes_status = {}
        mostrar_interface_distribuicao()

    except ValueError:
        mostrar_resultado("Erro", "Por favor, insira valores válidos.", altura_caixa=5, largura_caixa=40)

# Função para exibir a interface de distribuição de pontos com layout melhorado
def mostrar_interface_distribuicao():
    limpar_janela()

    # Cabeçalho centralizado
    tk.Label(root, text="Distribua Seus Pontos", font=("Arial", 14)).pack(pady=10)

    # Frame principal para centralizar os status
    frame_principal = tk.Frame(root)
    frame_principal.pack(pady=10)

    # Criando os labels, botões de setas e valores para cada status
    for nome, valor in status_atual.items():
        frame = tk.Frame(frame_principal)
        frame.pack(pady=5, anchor='w')  # Mantendo alinhado à esquerda

        # Status alinhado à esquerda (coluna 0)
        tk.Label(frame, text=f"{nome}: ", font=("Arial", 12), anchor="w", width=12).grid(row=0, column=0, padx=10, sticky='w')

        # Botão para diminuir o valor (coluna 1)
        btn_down = tk.Button(frame, text="⬇️", command=lambda n=nome: alterar_status(n, -1))
        btn_down.grid(row=0, column=1, padx=5)

        # Botão para aumentar o valor (coluna 2)
        btn_up = tk.Button(frame, text="⬆️", command=lambda n=nome: alterar_status(n, 1))
        btn_up.grid(row=0, column=2, padx=5)

        # Valor atual do status centralizado (coluna 3)
        label_valor = tk.Label(frame, text=f"{valor}", font=("Arial", 12), width=6)
        label_valor.grid(row=0, column=3, padx=10)

        # Guardando as referências para atualizações futuras
        botoes_status[nome] = {
            "label": label_valor,
            "btn_down": btn_down,
            "btn_up": btn_up
        }

    # Atualizar e exibir nível, HP e effort em tempo real
    atualizar_informacoes_extra()

    # Mostrar os pontos restantes centralizado abaixo dos status
    tk.Label(root, text=f"Pontos Restantes: {pontos_disponiveis}", font=("Arial", 12)).pack(pady=10)

    # Botão Voltar centralizado
    tk.Button(root, text="Voltar", command=mostrar_menu).pack(pady=20)

# Função para alterar o status e atualizar os pontos disponíveis
def alterar_status(nome, direcao):
    global pontos_disponiveis, status_atual

    valor_atual = status_atual[nome]
    custo_proximo = valor_atual + direcao

    # Verifica o custo para subir ou descer
    if direcao > 0:  # Aumentar status
        custo = calcular_soma_progressao_aritmetica(valor_atual, custo_proximo)
        if pontos_disponiveis >= custo:
            pontos_disponiveis -= custo
            status_atual[nome] += 1
    elif direcao < 0 and valor_atual > 0:  # Diminuir status
        custo = calcular_soma_progressao_aritmetica(custo_proximo, valor_atual)
        pontos_disponiveis += custo
        status_atual[nome] -= 1

    # Atualiza a interface
    mostrar_interface_distribuicao()

# Função para atualizar e exibir nível, HP e effort em tempo real
def atualizar_informacoes_extra():
    global status_atual, pontos_disponiveis

    # Cálculo do nível
    nivel = sum(status_atual.values())

    # Cálculo dos pontos de vida (HP)
    resistencia = status_atual.get("Resistência", 0)
    A = (resistencia // 10) * 0.3
    B = (nivel // 100) * 0.5
    X = A + B
    hp = int(nivel * (X + 1))

    # Cálculo do Effort
    effort_d12 = nivel // 60
    effort_d20 = nivel // 100
    effort_d50 = nivel // 250

    # Frame para exibir informações adicionais (nível, HP e Effort)
    frame_extra = tk.Frame(root)
    frame_extra.pack(pady=10)

    tk.Label(frame_extra, text=f"Nível: {nivel}", font=("Arial", 12)).pack(pady=5)
    tk.Label(frame_extra, text=f"HP: {hp}", font=("Arial", 12)).pack(pady=5)
    tk.Label(frame_extra, text=f"Effort: {effort_d12}d12, {effort_d20}d20, {effort_d50}d50", font=("Arial", 12)).pack(pady=5)

# Criando a janela principal
root = tk.Tk()
root.title("Calculadora de Status")


# Centralizando a janela
root_width = 500
root_height = 570
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f'{root_width}x{root_height}+{x}+{y}')

mostrar_menu()

root.mainloop()