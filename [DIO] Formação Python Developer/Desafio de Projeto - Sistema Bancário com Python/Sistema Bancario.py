from abc import ABC, abstractclassmethod, abstractproperty
import textwrap
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self.cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self.numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self,valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação Falhou! Você não tem Saldo Suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque Realizado com Sucesso!")
        else:
            print("\n@@@ Operação Falhou, o valor informado é invalido. @@@")
        return False

    def depositar(self, valor):
       if valor > 0:
        self._saldo += valor
        print("\n=== Deposito Realizado com Sucesso!===")
       else:
           print("\n@@@ Operação Falhou! o valor informado é inválido. @@@")
           return False
       return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print("\n@@@ Operação Falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação Falhou! Número Máximo de saque excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C\t\t{self.numero}
            Titula:\t{self.cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacoes(self, transacao):
        self.transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%s'),

            }

        )

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

        @property
        def valor(self):
            return self._valor

        def registrar(self, conta):
            sucesso_transacao = conta.sacar(self._valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacoes(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

        @property
        def valor(self):
            return self._valor

        def registrar(self, conta):
            sucesso_transacao = conta.depositar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacoes(self)


def menu():
    menu = '''\n
    =============== MENU ====================
     [1]\t Depositar
     [2]\t Sacar
     [3]\t Extrato
     [4]\t Novo Cliente
     [5]\t Nova conta
     [6]\t listar contas
     [0]\t Sair
    '''
    return input(textwrap.dedent(menu))

def deposito(clientes):
    cpf = input('Informe o CPF do Cliente: ')
    cliente = filtra_Usuario(cpf, clientes)

    if not cliente:
        print('\n @@@ cliente não encontrado! @@@')
        return
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def saque(clientes):

    cpf = input("informe o CPF do cliente: ")
    cliente = filtra_Usuario(cpf, clientes)

    if not cliente:
        print('\n @@@ Cliente não encontrado! @@@')
        return

    valor = float(input('Informe o valor do Saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def mostrar_extrato_(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtra_Usuario(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n ============= EXTRATO ============')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não Foram realizadas movimentações'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR${conta.saldo:.2f}")



def criar_cliente(clientes):
    cpf = input('informe o CPF: ')
    cliente = filtra_Usuario(cpf, clientes)

    if cliente:
        print('Usuario Já Cadastrado')
        return
    else:
        nome = input('Informe o nome Completo: ')
        data_nascimento = input('Informe a data de Nascimento (dd-mm-aaaa: ')
        endereco = input('Informe o endereço( Logradouro, nº - Bairro - Cidade/sigla estado): ')

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        clientes.append(cliente)

        print('\n === Cliente criado com sucesso! ====')



def filtra_Usuario(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n @@@ Cliente não possui conta! @@@')
        return
    # FIXME: Não permite cliente escolher a conta
    return cliente.conta[0]

def criar_conta(numero_conta, clientes, contas):

    cpf = input('Informe o CPF do Usuario: ')
    cliente = filtra_Usuario(cpf,clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado!@@@')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.conta.append(conta)

    print('\n === Clinta criada com sucesso! ===')


def lista_contas(contas):
    for conta in contas:
        print('='*100)
        print(textwrap.dedent(conta))

def main():
    cliente = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            deposito(cliente)
        elif opcao == '2':
            saque(cliente)
        elif opcao == '3':
            mostrar_extrato_(cliente)
        elif opcao == '4':
            criar_cliente(cliente)
        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,cliente,contas)
        elif opcao == '6':
            lista_contas(contas)
        elif opcao == '0':
            print('SISTEMA FINALIZADO, VOLTE SEMPRE!')
            break
        else:
            print('Opção Invalida, por favor selecione novamente a operação desejada')

main()