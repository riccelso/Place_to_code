import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
#from cleaner import cleaner

def naveg(csvpath, timewaited=6, intime=6, tryagain=20):
    '''
    :param csvpath: caminho do arquivo analisado
    :param timewaited: tempo de espera explicita do selenium
    :param intime:  tempo de espera implicita do selenium
    :param tryagain: numero de tentativas em caso de erro
    :return: dados da pesquisa aninhados em listas e dicionarios
    '''
    
    # INPUT
    arq = pd.read_csv(csvpath, dtype={'CPFs': 'object'})
    lines = arq['CPFs'].apply(str).str.replace('.', '').str.replace('-', '')

    # deletar posteriormente
    # código usado para embaralhar sequencia de cpfs usados
    from random import shuffle
    lines = lines.to_list()
    shuffle(lines)
    lines = pd.Series(lines)

    # regs
    links = []
    link = None
    again = 0
    random = 'randomtry'


    with webdriver.Firefox(executable_path=r"./geckodriver") as nav:
        nav.delete_all_cookies()
        # loop cpfs
        for cpf in lines.values:
            nav.get(f'http://www.portaltransparencia.gov.br/pessoa-fisica/busca/lista?termo={cpf}&pagina=1&tamanhoPagina=10')

            zero = ''
            try:
                print(f'Busca do cpf: {cpf}')
                WebDriverWait(nav, timewaited).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#resultados > li:nth-child(1) > h3')))

                look = nav.find_element_by_css_selector('strong.titulo-6--menor').text.strip()
                look = re.search(r'\d{3}\.\d{3}', look)[0].replace('.', '')
                if look not in cpf:
                    raise Exception

            except Exception:
                while 1:
                    try:
                        zero = nav.find_element_by_css_selector('div.col-sm-10.pull-center')
                        if zero:
                            zero = zero.text
                            if '0 resultados' in zero:
                                links.append({cpf: 'nr'})
                                print(f'0 resultados para o cpf {cpf}')
                                break
                            else:
                                zero = ''
                    except Exception:
                        pass

                    if again % 2 == 0:
                        nav.get(
                            f'http://www.portaltransparencia.gov.br/pessoa-fisica/busca/lista?termo={random}&pagina=1&tamanhoPagina=10')
                        nav.implicitly_wait(2.5)
                        nav.get(
                            f'http://www.portaltransparencia.gov.br/pessoa-fisica/busca/lista?termo={cpf}&pagina=1&tamanhoPagina=10')

                    try:
                        WebDriverWait(nav, timewaited).until(EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '#resultados > li:nth-child(1) > h3')))
                    except selenium.common.exceptions.TimeoutException:
                        print(f'Falha nº{again+1}')
                        if again == tryagain:
                            exit()
                        again += 1
                    else:
                        break

            nav.implicitly_wait(intime)
            print(f"Nº de repetições de busca: {again}")

            if not zero:
                element = nav.find_element_by_id('resultados'). \
                    find_element_by_css_selector('h3.titulo-3')
                link = element.find_element_by_tag_name('a').get_attribute('href')
                links.append({cpf: link})


        print(links)
        print(f'\nNúmero de links encontrados: {len(links)}')
        print(f'Número de cpfs solicitados: {len(lines.values)}')

        if link:
            del link
        del zero, element, again, lines, arq

        # 2ª etapa:
        nameColumns = set()
        nmlist = []
        e11 = e21 = e31 = e41 = ''


        for i, link in enumerate(links):
            print('\n' + '-'*20)

            # Para não recebedores
            if tuple(link.values())[0] == 'nr':
                id = tuple(link.keys())[0]
                print(id)
                nmlist.append({id: []})
                continue

            gt = tuple(link.values())[0]
            print(gt)
            nav.get(gt)

            #Verificar melhor format e escoher um dos dois abaixo

            WebDriverWait(nav, timewaited).until(EC.presence_of_element_located(
                (By.ID, 'group-1')))

            bts = nav.find_element_by_id('group-1'). \
                find_elements_by_tag_name('button')

            # ID
            id = tuple(link.keys())[0]
            print(f'ID: {id}')
            nmlist.append({id: []})

            x = nav.find_element_by_css_selector('body > main > div:nth-child(3)').get_attribute('innerHTML')
            # print(x)

            bts = tuple(re.finditer('<button id=".*?"', x))
            for i2, each in enumerate(bts):
                newp = find1 = find2 = None
                columname = each[0][12:-1].replace('btnAba', '')
                nameColumns.add(columname)


                if 'ViagensAServico' in each[0]:
                    print('Viagem a servico')
                    nmlist[i][id].append({columname: 'Recursos para viagens a servico'})
                    continue

                if bts[i2] == bts[-1]:
                    newp = x[bts[i2].start():]
                else:
                    newp = x[bts[i2].start():bts[i2 + 1].start()]

                find1 = tuple(re.finditer(r'<strong>.*?</strong>', newp))

                for el in find1:
                    print(el[0][8:-9])
                    if ':' in el[0]:
                        find2 = re.search(r'<span>.*?</span>', newp[el.start():])
                        print(find2[0][6:-7])
                        nmlist[i][id].append({columname: f'{el[0][8:-9]} {find2[0][6:-7]}'})
                        continue
                    find2 = re.search(r'R.?\s[0-9./]+?,\d\d', newp[el.start():])
                    if not find2:
                        nmlist[i][id].append({columname: f'{el[0][8:-9]}'})
                        continue
                    print(find2[0])
                    nmlist[i][id].append({columname: f'{el[0][8:-9]} {find2[0]}'})

    return nmlist, list(nameColumns)




def main(func):
    import cProfile, pstats

    with cProfile.Profile() as pr:
        func()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


if __name__ == '__main__':
    pass