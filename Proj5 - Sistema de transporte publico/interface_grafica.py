from getpass import getpass
from datetime import date
import sys
from keyboard import add_hotkey, press
from p2_classes import *
from string import punctuation
from rich import print as pprint
from rich import pretty
from rich.traceback import install
from rich.table import Table
from rich.console import Console
import os
from time import sleep
from colorama import Fore, Back, Style

pretty.install()
install()
os.system('cls')

# VARÁIVES GLOBAIS
FLUSH = 0.05 # variavel determinante de velocidade do terminal
gestor_bd = Gestor_de_bd()


# MENU INICIAL
def menu():
    global FLUSH

    while 1:
        print(f'{Fore.LIGHTMAGENTA_EX}SELECIONE A OPÇÃO DESEJADA:')
        pprint('\n1. Gerenciar usuários e cartões')
        pprint('\n2. Criar registro de novo motorista')
        pprint('\n3. Gerenciar frota')
        pprint('\n4. Consulta de dados')
        if FLUSH == 0:
            pprint('\n5. Ativar velocidade do terminal')
        else:
            pprint('\n5. Desativar velocidade do terminal')
        pprint('\n6. Sair')

        result = input(
            f"{Fore.YELLOW}\n\nDigite aqui >>>> {Fore.RESET}").strip()
        

        try:
            result = int(result)
            if not result in [1, 2, 3, 4, 5, 6]:
                raise Exception
            
        except Exception as er:
            print(
                "Por favor siga o número que indica uma das opções dentre as opções\n")
            sleep(FLUSH * 10)
            print('Precione ENTER para reiniciar')
            getpass(prompt="")
            logo_rapida()
        else:
            if result == 5:
                resp6()
                continue
            elif result == 6:
                FLUSH = 0
                os.system('cls')
                logo_rapida()
                print('Obrigado por sua atenção!')
                print(Style.RESET_ALL)
                os._exit(os.O_EXCL)

            break
    return result

# GERENCIAR USUÁRIO E CARTÃO
def resp1():
    while 1:
        try:
            logo_rapida()
            print(f'{Fore.LIGHTMAGENTA_EX}SELECIONE A OPÇÃO DESEJADA:')
            print(Style.RESET_ALL)
            a_la_megaman(f'{Fore.LIGHTBLUE_EX}1{Fore.RESET}. Criar novo usuário e cartão\n')
            a_la_megaman(f'{Fore.LIGHTBLUE_EX}2.{Fore.RESET} Criar novo cartão para usuário\n')
            a_la_megaman(
                f'{Fore.LIGHTBLUE_EX}3.{Fore.RESET} Gerenciar crédito em cartão\n')
            a_la_megaman(f'{Fore.LIGHTBLUE_EX}4.{Fore.RESET} Voltar ao menu principal\n')

            result = input(
                f"{Fore.YELLOW}\n\nDigite aqui >>>> {Fore.RESET}"
            ).strip()


            if not result in ['1', '2', '3', '4']:
                raise ValueError("Valor fora das opções disponibilizadas")
            result = int(result)

            if result == 4:
               os.system('cls')
               break


            opcoes = [
                novo_usuario_e_cartao,
                criar_cartao,
                gerenciar_credito
            ]

            opcoes[result - 1]()

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")

# CRIAR NOVO USUÁRIO E CARTÃO
def novo_usuario_e_cartao():
    while 1:
        try:
            resp = {
                'Nome':'',
                'Sobrenome':'sobrenome',
                'E-mail':'nome@email.com',
                'Bairro':'bairro',
                'Data de nascimento':'01-01-2000',
            }

            msgs_auxiliares = [
                '\nPor favor não use números\n',
                '\nPor favor não use números\n',
                '\nPor favor siga o padrão usuario@email.com ou .com.br\n',
                '',
                '\nPor favor siga o padrão dia-mes-ano\n'
            ]

            a_la_megaman("\nAs seguintes informações serão solicitadas para o cadastro")
            
            a_la_megaman(f"{Fore.RED}nome{Fore.RESET}, ", no_sep=True)
            a_la_megaman(f"{Fore.RED}sobrenome{Fore.RESET}, ", no_sep=True)
            a_la_megaman(f"{Fore.RED}e-mail{Fore.RESET}, ", no_sep=True)
            a_la_megaman(f"{Fore.RED}bairro{Fore.RESET}, ", no_sep=True)
            a_la_megaman(f"e {Fore.RED}data de nascimento{Fore.RESET}.")

            registro_dados(resp, msgs_auxiliares, Usuario)

            cartao_pos_usuario(resp)

        except KeyboardInterrupt:
            print(
                '\n',
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                'ou "ctrl+c" para forçar saída',
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")
            instrucoes()
        else:
            break

# CRIAÇÃO DO CARTÃO EM USUÁRIO EXISTENTE
def criar_cartao():
    while 1:
        try:
            a_la_megaman(f'\nDigite o código ID do usuário para solicitar um {Fore.RED}cartão extra')
            print(Style.RESET_ALL)
            id_proprietario = input(">>>>> ")

            if not id_proprietario.isnumeric():
                raise ValueError("ID do usuário deve ser numérico")

            # Verificar se id_proprietario existe na base de dados
            info_usuario = gestor_bd.ver_dados(
                'Usuario', 
                colunas=[
                    'ID',
                    'NOME',
                    'SOBRENOME',
                    'EMAIL',
                    'BAIRRO',
                    'DATA_NASC'
                ], 
                onde=f'ID={id_proprietario}')
            
            
            if not info_usuario:
                print(
                    f"{Back.RED}Usuário não cadastrado",
                    Style.RESET_ALL
                )
                raise KeyboardInterrupt
            

            solicitar_confirmacao()
            construtor_tabela(Usuario.cabecalho, info_usuario)
            getpass(prompt="")

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")
            instrucoes()

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")
            instrucoes()


        else:
            gerar_cartao(info_usuario[0], gestor_bd)
            os.system('cls')
            break

# GERENCIAR SALDO
def gerenciar_credito():
    while 1:
        try:
            logo_rapida()        
            a_la_megaman(
                f'\nDigite o código {Fore.RED}ID{Fore.RESET} do usuário', 
                no_sep=True
            )
            a_la_megaman(f' para gestão de {Fore.YELLOW}crédito')
            print(Style.RESET_ALL)
            id_proprietario = input(">>>>> ")

            if not id_proprietario.isnumeric():
                raise ValueError("ID do usuário deve ser numérico")
            id_proprietario = int(id_proprietario)

            # Verificar se id_proprietario existe na base de dados
            info_usuario = gestor_bd.ver_dados(
                'Usuario',
                onde=f'ID={id_proprietario}')

            if not info_usuario:
                print(
                    f"{Back.RED}Usuário não cadastrado",
                    Style.RESET_ALL
                )
                raise KeyboardInterrupt

            solicitar_confirmacao()
            construtor_tabela(Usuario.cabecalho, info_usuario)
            getpass(prompt="")

            # Vendo saldo atual
            info_credito = gestor_bd.ver_dados(
                'Cartao',
                onde=f'ID_PROPRIETARIO={id_proprietario}',
                colunas=['ID', 'QTD_CREDITO']
            )

            construtor_tabela(
                (
                    'ID Cartão',
                    'Crédito disponível'
                ),
                info_credito
            )

            ids_cartoes = [x[0] for x in info_credito]
            soma_credito = sum([x[-1] for x in info_credito])

            tabela = Table()
            tabela.add_column('Soma total')
            tabela.add_row(str(soma_credito))

            console = Console()
            console.print(tabela)

            a_la_megaman(
                "\nOs valores acima disponibilizados se ", no_sep=True)
            a_la_megaman("referem ao total de crédito da ", no_sep=True)
            a_la_megaman("conta do usuário.")

            print(f"Aperte {Fore.RED}ENTER{Fore.RESET} para continuar")
            getpass(prompt='')


            # Adicionando saldo
            a_la_megaman(
                f'\nDigite o {Fore.RED}valor{Fore.RESET} que deseja inserir'
            )
            a_la_megaman(
                f'Ambos os padrões {Fore.GREEN}10,00 {Fore.RESET}',
                no_sep=True
            )
            a_la_megaman(
                f'ou {Fore.BLUE}10.00{Fore.RESET} são aceitos'
            )

            valor = input('>>>>> ')

            # Busca de padrão
            padrao = re.findall(r'^\d+[.,]?\d{0,2}$', valor)

            if not padrao:
                raise ValueError("Valor deve ser inserido com padrão explicitado")
            valor = float(valor.replace(',', '.'))

            a_la_megaman(f"\nDigite o {Fore.RED}ID{Fore.RESET} do cartão que obtera o saldo:")

            id_cartao = input(">>>>> ").strip()

            if not id_cartao.isnumeric():
                raise ValueError("ID do cartão deve ser numérico")
            id_cartao = int(id_cartao)

            if not id_cartao in ids_cartoes:
                raise ValueError("ID do cartão deve pertencer ao usuário escolhido")

            credito_novo = soma_credito + valor

            gestor_bd.atualizar_dados(
                tabela='Cartao',
                identificador=id_cartao, 
                coluna_mudar='QTD_CREDITO', 
                valor_novo=credito_novo,
            )

            info_credito = gestor_bd.ver_dados(
                'Cartao',
                onde=f'ID={id_cartao}',
                colunas=['ID', 'QTD_CREDITO']
            )

            soma_credito = sum([x[-1] for x in info_credito])

            info_sucesso()
            construtor_tabela(
                list(Usuario.cabecalho) + ['Saldo total novo'],
                dados=(list(info_usuario[0]) + [soma_credito],)
            )
            print(f'Saldo adicionado: {valor}')
            getpass(prompt="")


        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")

        else:
            break

# REALIZAR REGISTRO DE MOTORISTA
def resp2():
    while 1:
        try:
            logo_rapida()
            instrucoes()
            resp = {
                "CNH": "",
                'Nome': 'Nome Generico',
                'Sobrenome': 'Sobrenome Generico',
                'Data de nascimento': '01-01-1990',
            }

            msgs_auxiliares = [
                '\nCNH deve conter 11 dígitos\n',
                '\nPor favor não use números\n',
                '\nPor favor não use números\n',
                '\nPor favor siga o padrão dia-mes-ano\n'
            ]

            registro_dados(resp, msgs_auxiliares, Motorista)
            
            info_usuario = gestor_bd.ver_dados(
                'Motorista', 
                limit=1,
                desc=True
            )

            os.system('cls')
            a_la_megaman(
                f'Informações de {Fore.RED}novo cadastro realizado:\n'
            )
            print(Style.RESET_ALL)

            info_sucesso()
            construtor_tabela(Motorista.cabecalho, info_usuario)
            getpass(prompt='')
            os.system('cls')

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")

        else:
            break

# GERENCIAMENTO DE FROTA
def resp3():
    while 1:
        try:
            logo_rapida()
            print(Fore.LIGHTYELLOW_EX)
            print("Gerenciamento de frota\n\n", Style.RESET_ALL)
            print(f'{Fore.LIGHTMAGENTA_EX}SELECIONE A OPÇÃO DESEJADA:')
            pprint('\n1. Registrar novo ônibus')
            pprint('\n2. Vizualizar frota')
            pprint('\n3. Voltar ao menu principal')

            result = input(
                f"{Fore.YELLOW}\n\nDigite aqui >>>> {Fore.RESET}")

            if not result in ['1', '2', '3']:
                raise ValueError("Opção escolhida incorretamente")
            
            result = int(result)
            if result == 1:
                novo_onibus()
                os.system("cls")
                continue
            elif result == 2:
                frota = gestor_bd.ver_dados(tabela='Onibus')
                if frota:
                    info_sucesso()
                    construtor_tabela(
                        Onibus.cabecalho, 
                        frota
                    )
                    getpass(prompt='')
                os.system("cls")
                continue

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")

        else:
            os.system('cls')
            break

# CRIAR NOVO ONIBUS
def novo_onibus():
    os.system('cls')

    resp = {
        'Placa': '',
        'Linha': '1',
        'Modelo do ônibus': 'modelo generico',
        'Ano de fabricação': '1982',
    }

    msgs_auxiliares = [
        '',
        '',
        '',
        'Use somente números',
        'Use somente números',
    ]

    # Coleta e verificação de ID de motorista
    a_la_megaman(
        f"Digite o {Fore.RED}ID{Fore.RESET} do {Fore.BLUE}motorista{Fore.RESET}:")
    print(Style.RESET_ALL)

    id_motorista = int(input(f">>>>> "))

    if id_motorista < 0:
        raise ValueError("ID de motorista incorreto")

    info_motorista = gestor_bd.ver_dados(
        'Motorista',
        onde=f'ID={id_motorista}'
    )

    if not info_motorista:
        raise ValueError("ID de motorista não encontrado no sistema")

    resp['ID do motorista'] = id_motorista

    # Visualizar motorista
    solicitar_confirmacao()
    construtor_tabela(
        Motorista.cabecalho,
        dados=info_motorista
    )
    getpass(prompt="")

    # Coleta de dados para criar novo registro na frota
    a_la_megaman(
        "\nAs seguintes informações serão solicitadas para o cadastro")

    for v in tuple(resp.keys())[:2]:
        a_la_megaman(f"{Fore.RED}{v}{Fore.RESET}, ", no_sep=True)
    a_la_megaman(f"{Fore.RED}Modelo de ônibus{Fore.RESET} ", no_sep=True)
    a_la_megaman(f"e {Fore.RED}Ano de fabricação{Fore.RESET}.")

    resp = registro_dados(resp, msgs_auxiliares, Onibus,
                          ignorar=['ID do motorista'])

    a_la_megaman("Registro de onibus adicionado com sucesso")
    a_la_megaman("Informações de Onibus e Motorista abaixo:")

    dados = gestor_bd.ver_dados(
        'Onibus',
        limit=1,
        desc=True
    )

    construtor_tabela(Onibus.cabecalho, dados)

    a_la_megaman(f"Pressione ENTER para voltar ao {Fore.RED}menu principal")
    print(Style.RESET_ALL)
    getpass(prompt="")
    os.system('cls')

# CONSULTA DE DADOS
def resp4():
    while 1:
        try:
            logo_rapida()
            print(Fore.YELLOW)
            print('Consulta de dados')
            print(Fore.RESET)

            opcoes = (
                Usuario,
                Cartao,
                Motorista,
                Onibus,
            )

            a_la_megaman('Selecione uma opção para consulta de dados:')
            print('Ou responda 5 para voltar ao menu principal')
            print(Fore.BLUE)
            a_la_megaman(f'1{Fore.RESET}. Usuário\n')
            print(Fore.BLUE, end='')
            a_la_megaman(f'2{Fore.RESET}. Cartao\n')
            print(Fore.BLUE, end='')
            a_la_megaman(f'3{Fore.RESET}. Motorista\n')
            print(Fore.BLUE, end='')
            a_la_megaman(f'4{Fore.RESET}. Ônibus\n')

            resp_1  = input('\n>>>>> ')

            if not (resp_1 in ['1', '2', '3', '4', '5']):
                raise ValueError("Resposta não está dentre as opções disponibilizadas")
            elif resp_1 == '5':
                os.system('cls')
                break

            resp_1 = int(resp_1)
            
            classe_escolhida = opcoes[resp_1 - 1]

            a_la_megaman('\nQual coluna deseja filtrar:\n')
            
            for i, v in enumerate(classe_escolhida.cabecalho):
                print(Fore.BLUE, end='')
                a_la_megaman(f'{i+1}{Fore.RESET}. {v}\n')
            print()

            resp_2 = int(input('\n>>>>> '))

            if not ((resp_2) in range(1, len(classe_escolhida.cabecalho) + 1)):
                raise ValueError(
                    "Resposta não está dentre as opções disponibilizadas")

            coluna = tuple(classe_escolhida.cabecalho)[resp_2 - 1]
            coluna_sql = classe_escolhida.cabecalho[coluna]

            a_la_megaman(f'\nQual valor filtrará a coluna "{coluna.lower()}":')

            resp_3 = input('\n>>>>> ')

            info_usuario = gestor_bd.ver_dados(
                classe_escolhida.__name__,
                onde=f"{coluna_sql} LIKE '%{resp_3}%'"
            )

            print(f'\nAperte {Fore.RED}ENTER{Fore.RESET} para continuar\n')
            construtor_tabela(classe_escolhida.cabecalho, info_usuario)
            getpass(prompt='')
            os.system('cls')

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")

        else:
            break

# CONTROLAR FLUIDEZ
def resp5():
    global FLUSH
    if FLUSH > 0:
        FLUSH = 0
        os.system('cls')
    else:
        FLUSH = 0.05
        a_la_megaman('Fluidez do terminal ativada!!!')
        os.system('cls')
    logo_rapida()

# FUNÇÃO INTERMEDIARIA PARA INPUTS
def registro_dados(resp, msgs_auxiliares, Classe, ignorar=tuple()):
    while 1:
        try:
            # Loop para inputs:
            registro_novo = inputs(resp, msgs_auxiliares, Classe, ignorar)

            # Mostrar ao usuário os valores digitados:
            os.system('cls')
            solicitar_confirmacao()

            for k, v in resp.items():
                print(k, f'->{Fore.LIGHTBLUE_EX}', v, f'{Style.RESET_ALL}')
            
            getpass(prompt='')

        except KeyboardInterrupt:
            print(
                '\n',
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                'ou "ctrl+c" para forçar saída',
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")
            instrucoes()
        else:
            break
    
    gestor_bd.enviar_dados(registro_novo)
    return resp

# FUNÇÃO DE AUXÍLIO
def inputs(dicio, msgs_auxiliares, Classe, ignorar):
    for value, msg in zip(dicio.keys(), msgs_auxiliares):
        if value in ignorar: continue

        while 1:
            try:
                if not (value in ['Data de nascimento', 'Linha', 'Placa']):
                    a_la_megaman(
                        f"\nDigite seu {Fore.RED}{value.lower()}{Fore.RESET},"
                    )
                else:
                    a_la_megaman(
                        f"\nDigite sua {Fore.RED}{value.lower()}{Fore.RESET},"
                    )

                a_la_megaman(f"{msg}")

                dicio[value] = input(">>>>> ")

                Classe(*dicio.values())
            except ValueError as er:
                a_la_megaman(f'{Back.RED}{er}{Style.RESET_ALL}')
                print(
                    "Aperte ENTER para confirmar mensagem lida",
                    Fore.BLACK
                )
                print(Style.RESET_ALL)
                getpass(prompt='')
                os.system('cls')
                instrucoes()

            except KeyboardInterrupt:
                iter_print(
                    '\n',
                    f"{Back.RED}Reiniciando etapa, aperte ENTER para seguir em frente",
                    Style.RESET_ALL
                )
                getpass(prompt='')
                os.system("cls")
                instrucoes()

            else:
                break

    return Classe(*dicio.values())

# CRIAÇÃO DO CARTÃO
def gerar_cartao(info_usuario, gestor_bd):
    while 1:
        try:
            if len(info_usuario) > 1:
                id_proprietario = info_usuario[0]

            opcoes = (
                (1, 'comum'),
                (2, 'estudante'),
                (3, 'vale-transporte'),
                (4, 'idoso')
            )

            opcoes = dict(opcoes)

            a_la_megaman("Selecione o tipo do cartâo:\n")
            print(f"{Fore.RED}1.{Fore.LIGHTRED_EX} {opcoes[1]}{Style.RESET_ALL},")
            print(f"{Fore.RED}2.{Fore.LIGHTRED_EX} {opcoes[2]}{Style.RESET_ALL},")
            print(f"{Fore.RED}3.{Fore.LIGHTRED_EX} {opcoes[3]}{Style.RESET_ALL},")
            print(f"e {Fore.RED}4.{Fore.LIGHTRED_EX} {opcoes[4]}{Style.RESET_ALL}\n")

            resp = int(input(">>>> ").strip())
            print()
            if resp < 1 and resp > 4:
                raise ValueError("Valor não está entre as opções permitidas")

            idade = (date.today() - info_usuario[-1]).days / 360

            if (resp == 4) and (idade < 60):
                print(Back.RED)
                raise ValueError(
                    f"Para escolher a opção 4 a idade deve ser de pelo menos 60 anos{Style.RESET_ALL}"
                )

            cartao_novo = Cartao(id_proprietario, 0, opcoes[resp])
            gestor_bd.enviar_dados(cartao_novo)

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")
            instrucoes()

        except KeyboardInterrupt:
            iter_print(
                '\n',
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")
            instrucoes()

        else:
            id_cartao = gestor_bd.ver_dados("Cartao", limit=1, desc=True)[0][0]

            a_la_megaman(
                f"{Fore.BLUE}Cartão registrado com sucesso{Style.RESET_ALL}")
            a_la_megaman(
                f"O código identificador do seu cartão é {Fore.RED}{id_cartao}")
            print(Style.RESET_ALL)

            break

    a_la_megaman('Aperte ENTER para voltar ao menu principal')
    getpass(prompt='')
    os.system('cls')

# GERADOR DE RICH-TABELA
def construtor_tabela(cabecalho, dados):
    while 1:
        try:
            tabela = Table(title='Dados')
            for v in cabecalho:
                tabela.add_column(v)

            for d in dados:
                d = [
                    str(x) if type(x) != date else
                    (datetime(x.year, x.month, x.day)).strftime(r'%d/%m/%Y')
                    for x in d
                ]

                tabela.add_row(*d)

            terminal = Console()
            terminal.print(tabela)

        except ValueError as er:
            print(er)
            print("Aperte 'Enter' para continuar")
            getpass(prompt='')
            os.system("cls")
            instrucoes()

        except KeyboardInterrupt:
            iter_print(
                f"{Back.RED}Reiniciando processo, aperte ENTER para seguir em frente",
                Style.RESET_ALL
            )
            getpass(prompt='')
            os.system("cls")
            instrucoes()


        else:
            break

# CRIAR CARTÃO PARA USUÁRIO EXISTENTE
def cartao_pos_usuario(resp):
    # GESTOR DEVE BUSCAR ID DO USUÁRIO PARA CRIAR CARTÃO E VINCULAR A ELE
    dados = gestor_bd.ver_dados('Usuario',
                                limit=1,
                                desc=True
                                )

    os.system("cls")

    a_la_megaman(
        [
            f"{Back.RED}ATENÇÃO!!!{Back.RESET}{Fore.RED}\n",
            f'ANOTE SEU ID PARA ACESSO POSTERIOR\n{Style.RESET_ALL}',
            '\nID do usuário:\n',
            str(dados[0][0]),
        ]
    )

    info_sucesso()
    construtor_tabela(Usuario.cabecalho, dados)
    getpass(prompt='')

    Style.RESET_ALL
    sleep(0.5)
    gerar_cartao(dados[0], gestor_bd)

# ITERA E PRINTA
def iter_print(*args):
    print('\n', *args, Style.RESET_ALL, '\n', sep='')

# LIMPAR E PRINTAR LOGO
def logo_rapida():
    os.system('cls')
    print(Fore.LIGHTBLUE_EX, poccosystem_logo, Style.RESET_ALL)

# PRINT DE INSTRUÇÕES
def instrucoes():
    iter_print(
        f"{Back.BLACK}Aperte 'ctrl+a' para acelerar o terminal"
    )
    iter_print(
        f"{Back.BLACK}Segure 'ctrl+a' para desligar fluidez do terminal"
    )
    iter_print(
        f"{Back.BLACK}Aperte 'ctrl+c' para reiniciar o terminal neste processo",
    )

# APERTE ENTER PARA CONFIRMAR
def solicitar_confirmacao():
    print(
        f"\n\nPor favor aperte {Fore.RED}\"Enter\"{Fore.RESET} para confirmar")
    print("Caso considere algo de errado com as informações", end=', ')
    print(f"reinicie o processo com '{Fore.RED}ctrl+c{Fore.RESET}'\n")

# PRINT SOBRE INFORMAÇÃO DISPONIBILIZADA COM SUCESSO
def info_sucesso():
    print("\n\nInformação disponibilizada com sucesso")
    print(
        f"Por favor aperte {Fore.RED}\"Enter\"{Fore.RESET} para continuar")

# PRINT COMO MEGAMAN
def a_la_megaman(msg, no_sep=False):
    # https://www.youtube.com/watch?v=VQI1I7L3BCo
    for each in msg:
        if not each in punctuation:
            print(each, end='', flush=True)
            sleep(FLUSH)
        else:
            print(each, end='', flush=True)
            sleep(FLUSH)
    Style.RESET_ALL
    if not no_sep:
        print()

# FUNÇÃO PARA VINCULAR A ATALHO 'CTRL + A'
def mudar_velocidade():
    global FLUSH
    FLUSH = FLUSH ** 2

# FUNÇÃO PRINCIPAL
def main():
    global FLUSH
    add_hotkey("ctrl+a", mudar_velocidade)

    print(Fore.LIGHTBLUE_EX)

    for trecho in [bem, vindo, ao, poccosystem_logo]:
        print(trecho, sep='', end='', flush=True)
        sleep(FLUSH * 10)

    print(Fore.RESET)

    pprint('por: blueshift brasil')
    pprint("~"*80)
    sleep((FLUSH ** 2) * 10)
    pprint()

    while 1:
        result = menu()
        print('\n')
        sleep((FLUSH ** 3) * 10)

        iter_print(f"{Back.BLACK}Aperte 'ctrl+a' para acelerar o terminal")
        iter_print(
            f"{Back.BLACK}Segure 'ctrl+a' para desligar fluidez do terminal")

        a_la_megaman("\n  Opção selecionada:")
        sleep((FLUSH ** 3) * 10)

        a_la_megaman(
        fr"""
                 ____
                ||{result} ||
                ||__||
                |/__\|
                    """
        )

        iter_print(
            f"{Back.BLACK}Aperte 'ctrl+c' para reiniciar o terminal neste processo",
        )

        print("\nPressione ENTER para prosseguir")
        getpass(prompt='')
        os.system('cls')
        exec(f"resp{result}()")
        logo_rapida()


bem = \
r"""
    ____                 
   / __ )___  ____ ___   
  / __  / _ \/ __ `__ \  
 / /_/ /  __/ / / / / /  
/_____/\___/_/ /_/ /_/
"""

vindo = \
r"""
          _           __     
   _   __(_)___  ____/ /___  
  | | / / / __ \/ __  / __ \ 
  | |/ / / / / / /_/ / /_/ / 
  |___/_/_/ /_/\__,_/\____/                               
"""

ao = \
r"""
      ____ _____ 
     / __ `/ __ \
    / /_/ / /_/ /
    \__,_/\____/ 
"""

poccosystem_logo = \
r"""
                               _____                 
______________________  _________  /____________ ___ 
___  __ \ / ___/_  / / /_  ___/  __/  _ \_  __ `__ \
__  /_/ /(__  )_  /_/ /_(__  )/ /_ /  __/  / / / / /
_  .___/ ____/ _\__, / /____/ \__/ \___//_/ /_/ /_/ 
/_/               /_/
                                                                          
"""

if __name__=="__main__":
    main()