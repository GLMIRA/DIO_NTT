import os

menu = """
[s] Saque
[d] Deposito
[e] Extrato
[q] sair
"""
opcao = ""
VALOR_LIMITE_SAQUE = 500.00
LIMITE_SAQUE_DIARIO = 3
saldo = 0.0
num_saques = 0
operacoes = []


def valida_valor_digitado(valor_digitado: str):
    while True:
        try:
            return float(valor_digitado)
        except ValueError:
            print("Valor digitado é inválido.")
            valor_digitado = input("Digite novamente: ")


def extrato_bancario(saldo, operacoes: list) -> str:
    print("Seu Extrato esta aqui ")
    print("*" * 30)
    for operacao in operacoes:
        tipo_operacao, valor = operacao
        print(f"Operação: {tipo_operacao.capitalize()}")
        print(f"Valor: R$ {valor:.2f}")
        print("-" * 30)

    print(f"seu saldo atual é de: R${saldo:.2f}")
    print("*" * 30)


def deposito_bancario(saldo: float, operacoes: list) -> float:
    def recebe_valor_deposito() -> float:
        valor_digitado = input("digite o valor que voce deseja depositar: ")
        valor_deposito = valida_valor_digitado(valor_digitado=valor_digitado)
        print(valor_deposito)
        return valor_deposito

    def verifica_se_valor_e_positivo(valor_deposito: float) -> bool:
        """valida se o deposito nao é em um valor negativo

        Args:
            valor_deposito (float): valor do deposito

        Returns:
            bool: retorna verdadeiro se for negitvo e false se for positivo
        """
        return valor_deposito < 0

    def fazendo_o_deposito(valor_deposito: float, saldo: float):
        novo_saldo = saldo + valor_deposito
        return novo_saldo

    def adiciona_deposito_em_operacoes(valor_deposito: float, operacoes: list) -> bool:
        try:
            operacoes.append(("deposito", valor_deposito))
            return True
        except:
            return False

    valor_deposito = recebe_valor_deposito()
    if verifica_se_valor_e_positivo(valor_deposito):
        return "o valor do deposito nao pode ser negativo", saldo
    if not adiciona_deposito_em_operacoes(
        valor_deposito=valor_deposito, operacoes=operacoes
    ):
        return "erro ao fazer o deposito ", saldo

    novo_saldo = fazendo_o_deposito(valor_deposito=valor_deposito, saldo=saldo)

    return (
        f"deposito no valor de {valor_deposito:.2f} realizado com sucesso, "
        f"seu saldo é de {novo_saldo:.2f}",
        novo_saldo,
    )


def saque_bancario(
    saldo: float,
    VALOR_LIMITE_SAQUE: int,
    LIMITE_SAQUE_DIARIO: int,
    num_saques: int,
    operacoes: list,
) -> str:
    """funçaao para realizar um saque bancario

    Args:
        saldo (float): saldo atual do cliente
        VALOR_LIMITE_SAQUE (int): valor limite que o cliente pode sacar
        LIMITE_SAQUE_DIARIO (int): valor de saque diario do cliente
        num_saques (int): numero de saques realizados pelo cliente
        operacoes (list): uma lista de operaçoes é atulizada a cada saque

    Returns:
        str: retorna uma mensagem, e atualiza o valor que foi digitado
    """

    def recebe_o_valor_saque() -> float:
        """solicita o valor que usuario deseja sacar,
            chama a funçao que valida se o valor digitado pode ser convertido
            para float
        Returns:
            float: o valor que o suario deseja sacar
        """

        valor_digitado = input("digite o valor que deseja sacar: ")
        valor_saque = valida_valor_digitado(valor_digitado=valor_digitado)
        return valor_saque

    def verifica_limite_saque(valor_saque: float) -> bool:
        """'verifca se o valor que sera sacado esta dentro do limite
            do valor maximo que pode ser sacado

        Returns:
            bool: True se ele puder sacar False se não ele puder sacar
        """
        return valor_saque <= VALOR_LIMITE_SAQUE

    def verifica_limite_saques_diarios(num_saques: int) -> bool:
        """Verifica se o número de saques diários foi alcançado.

        Returns:
            bool: retorna True se o saque que esta sendo feito
            esta dentro do limite de saque diario.

        """
        return num_saques < LIMITE_SAQUE_DIARIO

    def valor_na_conta(valor_saque: float, saldo: float) -> bool:
        """valida se o valor que ele esta tentando sacar existe na conta dele

        Args:
            valor_saque (float): valor que ele deseja sacar
            saldo (float): quanto ele tem na conta
        Returns:
            bool: retorna verdade se ele puder sacar false se ele nao puder
            sacar o valor
        """
        return round(valor_saque, 2) <= round(saldo, 2)

    def desconta_valor_da_conta(valor_saque: float, saldo: float) -> float:
        """desconta o valor da conta do cliente

        Args:
            valor_saque (float): _description_
            saldo (float): _description_

        Returns:
            float: _description_
        """
        return saldo - valor_saque

    def refatora_informacoes_apos_saque(
        operacoes: list,
        valor_saque: float,
        num_saques: int,
    ) -> int:
        """refatora o valor de numeros de saques
            adicioan uma tupla dentro da lista operações(
            tipo de operção que é uma str e um float com o valor que foi sacado)

        Args:
            operacoes (list): lista com todas as operaçoes bancarias realizado
            valor_saque (float): valor que foi sacado pelo usuario
            num_saques (int): numero de saques que o usuario pode fazer

        Returns:
            int: numero de saques atualizado
        """

        operacoes.append(("saque", valor_saque))
        num_saques += 1
        return num_saques

    valor_saque = recebe_o_valor_saque()

    if not verifica_limite_saque(valor_saque=valor_saque):
        return "valor maior que o limite de saque", saldo, num_saques

    if not verifica_limite_saques_diarios(num_saques=num_saques):
        return "limite de saques excedido", saldo, num_saques

    if not valor_na_conta(valor_saque=valor_saque, saldo=saldo):
        return "saldo insuficiente", saldo, num_saques

    if valor_saque < 0:
        return "o valor do saque nao pode ser negativo", saldo, num_saques
    saldo = desconta_valor_da_conta(valor_saque=valor_saque, saldo=saldo)

    num_saques = refatora_informacoes_apos_saque(operacoes, valor_saque, num_saques)

    return (
        f"saque no valor de {valor_saque:.2f}, realizado com sucesso "
        f"o seu saldo agora é no valor de {saldo:.2f}",
        saldo,
        num_saques,
    )


while True:
    print("SEJA BEM VINDO, COMO PODEMOS TE AJUDAR HOJE")
    opcao = input(menu)

    if opcao == "e":
        print()
        extrato_bancario(saldo, operacoes)

    elif opcao == "s":
        mensagem, saldo, num_saques = saque_bancario(
            saldo, VALOR_LIMITE_SAQUE, LIMITE_SAQUE_DIARIO, num_saques, operacoes
        )
        print(mensagem)

    elif opcao == "d":
        mensagem, saldo = deposito_bancario(saldo, operacoes)
        print(mensagem)

    elif opcao == "q":
        os.system("clear")
        print("saindo")
        break

    else:
        print("digite uma opcao valida")
