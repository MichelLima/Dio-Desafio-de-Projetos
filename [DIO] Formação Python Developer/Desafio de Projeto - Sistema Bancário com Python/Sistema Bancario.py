'''
Criar um Sistema bancario com as Operações de:
- Déposito;
- Saque;
- Extrato.
'''
import textwrap

''''
DEPOSITO:
-DEPOSITAR APENAS VALORES POSITIVOS NA CONTA;
- V1 DO SISTEMA, NÃO PRECISA DE DADOS DA CONTA;
- TODOS OS DEPOSITOS DEVEM SER ARMAZENADOS EM UMA VARIÁVEL E EXIBIDOS NA OPERAÇÃO DE EXTRATO. 

SAQUE: 
- lIMITE DE 3 SAQUES DIARIOS;
- LIMITE DE R$ 500,00 POR SAQUE;
- SE O USUARIO NÃO TEM LIMITE O SISTEMA INFORMA QUE NÃO SERÁ POSSIVEL SACAR DINHEIRO POR FALTA DE SALDO;
- TODOS OS SAQUES DEVEM SER ARMAZENADOS EM UMA VARIÁVEL E EXIBIDOS NA OPERAÇÃO DE EXTRATO; 

EXTRATOS:
- LISTAR TODOS OS DEPÓSITOS E SAQUES REALIZADOS NA CONTA;
- NO FINAL DO EXTRATO EXIBIR O SALDO ATUALIZADO DA CONTA;
- OS VALORES DEVEM SER EXIBIDOS NO FORMATO R$ XXX.XX
'''

menu = '''
 [1] Depositar
 [2] Sacar
 [3] Extrato
 [4] Novo Usuario
 [5] Nova conta
 [6] listar contas
 [0] Sair
'''
def deposito(saldo, valorDeposito, extrato, /):

    saldo += valorDeposito
    extrato += f'Depósito: R$ {valorDeposito:.2f}\n'
    print('Deposito Realizado com Sucesso!')
    print('--------------------------------')
    return saldo, extrato

def saque(*, saldo, valorSaque, extrato, limite_diario, numero_saques, limite_Saque):

    if numero_saques >= limite_Saque:  # LIMITE DE SAQUES DIARIOS ATIGINDOS
        print('Operação Falhou, você atingiu o limite diario de saques !')

    elif valorSaque > limite_diario:  # VALOR MAIOR QUE LIMITE DIARIO
        print('Operação Falhou, valor do saque maior que o limite diario!')

    elif valorSaque > saldo:  # SEM SALDO
        print('Operação Falhou, você não tem saldo suficiente!')

    elif valorSaque > 0:
        saldo -= valorSaque
        numero_saques += 1
        extrato += f'Saque: R$ {valorSaque:.2f}\n'
    else:
        print('Operação Falhou, O valor informado é invalido!')

    return saldo, extrato

def mostrar_extrato_(saldo,/,*, extrato):
    print('=================EXTRATO==================')
    if extrato == ' ':
        print('Não foram realizados Movimentações.')
    else:
        print(extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print('============================================')

def criar_usuario(usuarios):
    cpf = input('informe o CPF: ')
    usuario = filtra_Usuario(cpf, usuarios)

    if usuario:
        print('Usuario Já Cadastrado')
        return
    else:
        print('Usuario não cadastrado')
        nome = input('Informe o nome completo: ')
        data_nacimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
        endereco = input('Informe o endereco(logradouro, nº - bairro - cidade/sigla estado: ')

        usuarios.append({'nome': nome, 'data_nascimento': data_nacimento, 'cpf': cpf, 'endereco': endereco})
        print('Usuario Cadastrado com Sucesso!!!')



def filtra_Usuario(cpf, usuario):

    for usuario in usuarios:
        if usuario['cpf'] == cpf:
           return usuarios
    return None

def criar_conta(agencia, numero_conta, usuarios):
     cpf = input('Informe o CPF do Usuario: ')
     usuario = filtra_Usuario(cpf,usuarios)

     if usuario:
         print('Conta criada com sucesso!')
         return {'agencia':agencia, 'numero_conta': numero_conta, 'usuario': usuario}
     print('Usuario não encontrado!')

def lista_contas(contas):
    for conta in contas:
        linha = f''' \
                Agencia:\t{conta['agencia']}
                C/C: \t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
                '''
        print('='*100)
        print(textwrap.dedent(linha))

saldo = 0
limite_diario = 500
extrato = ' '
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []
AGENCIA = '0001'


while(True):

    while(True):

        opcao = input(f'{menu} Selecione uma Opção do Menu: ')

        if opcao in '1234560':
            break
        else:
            print('Opção Invalida!')

    if opcao == '1':

            try:
                valorDeposito = float(input('Digite o valor para Déposito: '))
                if valorDeposito > 0:

                    saldo, extrato = deposito(saldo, valorDeposito, extrato)

                else:
                    print('Operação Falhou, Digite um Valor Valido')

            except ValueError:
                print('Operação Falhou, Digite um Valor Numerico Valido')

    elif opcao == '2':

        try:
            valorSaque = float(input('Digite o valor para Saque: '))

            saldo, extrato = saque(saldo=saldo,
                                   valorSaque=valorSaque,
                                   extrato=extrato,
                                   limite_diario=limite_diario,
                                   numero_saques=numero_saques,
                                   limite_Saque=LIMITE_SAQUES)


        except ValueError:
            print('Operação Falhou, Digite um Valor Numerico Valido')

    elif opcao == '3':

     mostrar_extrato_(saldo, extrato=extrato)

    elif opcao == '4':
        criar_usuario(usuarios)

    elif opcao == '5':
      numero_conta = len(contas)+1
      conta = criar_conta(AGENCIA, numero_conta, usuarios)

      if conta:
          contas.append(conta)

    elif opcao == '6':
          lista_contas(contas)

    elif opcao == '0':
        print('SISTEMA FINALIZADO, VOLTE SEMPRE!')
        break
    else:
        print('Opção Invalida, por favor selecione novamente a operação desejada')