import PySimpleGUI as sg
import numpy as np
from itertools import count
from os.path import exists
import json

# Estrutura
espacos = 45

estrutura = np.arange(1, espacos + 1)
estrutura = estrutura.reshape((estrutura.shape[0] // 5), 5)


# Região do corredor
corredor = [2, 3, 4, 5]
corredor = corredor + np.arange(8, espacos, 5).tolist()


# Verificar compras realizadas:
if exists('./compra_realizada.json'):
    with open('./compra_realizada.json', 'r') as arq:
        selecionados = json.load(arq)
else:
    selecionados = dict()



# Etiqueta poltronas
etiqueta = count(start=1)

composicao_botoes = []
botoes = []
for fila in estrutura:
    for vaga in fila:
        if vaga == 1:
            # Motorista
            botoes.append(sg.Column([[sg.T(s=4, background_color='#007080')]]))
        elif vaga in corredor:
            botoes.append(sg.Column([[sg.T(s=4)]])) # Corredor
        else:
            if str(vaga) in selecionados.keys():
                botoes.append(sg.Button(f'{str(next(etiqueta)).zfill(2)}', key=vaga, button_color=('#FFFFFF', '#838383')))
                continue
            botoes.append(sg.Button(f'{str(next(etiqueta)).zfill(2)}', key=vaga))
    composicao_botoes.append(botoes[:])
    botoes = []





sg.theme('DarkAmber') # Tema

# Composição da janela
layout = [
    [sg.Text('Selecione o(s) acento(s) que deseja comprar:')],
    composicao_botoes,
    [sg.Button('Comprar', key='-b-'), sg.Button('Limpar', key='-cls-')]
]



# Nova janela
window = sg.Window('PoccoBus', layout)

# Seleção temporária:
selec_temp = dict()

# App
while 1:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # Fechamento de janela
        # import pdb
        # pdb.set_trace()

        # RELATÓRIO FINAL
        with open("./relatorio_final.txt", 'w') as f:
            # Título do relatório
            relatorio = 'Relatório sobre poltronas:\n'

            # Append nos botões e seus respectivos estados
            for fila in composicao_botoes:
                for botao in fila:
                    if hasattr(botao, "ButtonText"):
                        if botao.ButtonText in selecionados.values():
                            relatorio += f"poltrona {botao.ButtonText} indisponível\n"
                        else:
                            relatorio += f"poltrona {botao.ButtonText} disponível\n"

            f.write(relatorio)
        break

    elif isinstance(event, np.int64):
        if window[event].ButtonColor[1] == '#283b5b':
            window[event].Update(button_color=('#FFFFFF', 'red'))
            selec_temp[int(event)] = window[event].ButtonText
        elif window[event].ButtonColor[1] == 'red':
            selec_temp[int(event)] = window[event].ButtonText
            window[event].Update(button_color=('#FFFFFF', '#283b5b'))

        window.refresh()


    elif event == '-b-':
        # Gerar relatório
        with open('./compra_realizada.json', 'w') as arq:
            selecionados.update(selec_temp)
            json.dump(selecionados, arq)
        
        sg.popup('Compra realizada com sucesso!', auto_close=True, auto_close_duration=3)

        window.close()


    elif event == '-cls-':
        for each in selec_temp.keys():
            if window[each].ButtonColor[1] == 'red':
                window[each].Update(button_color=('#FFFFFF', '#283b5b'))
                selec_temp = dict()
           

window.close()