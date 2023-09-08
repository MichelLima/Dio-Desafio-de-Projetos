'''
Criar um Sistema bancario com as Operações de:
- Déposito;
- Saque;
- Extrato.
'''

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
 [0] Sair
'''

saldo = 0
limite_diario = 500
extrato = ' '
numero_saques = 0
LIMITE_SAQUES = 3
'''

'''
while(True):

    while(True):

        opcao = input(f'{menu} Selecione uma Opção do Menu: ')

        if opcao in '1230':
            break
        else:
            print('Opção Invalida!')

    if opcao == '1':

            try:
                valorDeposito = float(input('Digite o valor para Déposito: '))

                if valorDeposito > 0:

                    saldo += valorDeposito
                    extrato += f'Depósito: R$ {valorDeposito:.2f}\n'
                    print('Deposito Realizado com Sucesso!')
                    print('--------------------------------')
                else:
                    print('Operação Falhou, Digite um Valor Valido')

            except ValueError:

                print('Operação Falhou, Digite um Valor Numerico Valido')

    elif opcao == '2':

        try:
            valorSaque = float(input('Digite o valor para Saque: '))

            if numero_saques >= LIMITE_SAQUES: #LIMITE DE SAQUES DIARIOS ATIGINDOS
                print('Operação Falhou, você atingiu o limite diario de saques !')

            elif valorSaque > limite_diario: #VALOR MAIOR QUE LIMITE DIARIO
                print('Operação Falhou, valor do saque maior que o limite diario!')

            elif valorSaque > saldo: #SEM SALDO
                print('Operação Falhou, você não tem saldo suficiente!')

            elif valorSaque > 0:
                saldo -= valorSaque
                numero_saques += 1
                extrato += f'Saque: R$ {valorSaque:.2f}\n'
            else:
                print('Operação Falhou, O valor informado é invalido!')

        except ValueError:
            print('Operação Falhou, Digite um Valor Numerico Valido')

    elif opcao == '3':

      print('=================EXTRATO==================')
      if extrato == ' ':
        print('Não foram realizados Movimentações.')
      else:
          print(extrato)
          print(f'\nSaldo: R$ {saldo:.2f}')
          print('============================================')

    elif opcao == '0':
        print('SISTEMA FINALIZADO, VOLTE SEMPRE!')
        break
    else:
        print('Opção Invalida, por favor selecione novamente a operação desejada')