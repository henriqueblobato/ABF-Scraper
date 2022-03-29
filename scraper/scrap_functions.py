import re
import json
from datetime import datetime

import django
django.setup()

import requests
from bs4 import BeautifulSoup

from api_ap.models import (
    Url,
    FranchiseType,
    Franchise,
    State,
)

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

money_regex = r'\$\d+(?:\.\d+)?'  # \$\d+(?:\.\d+)?
regex = re.compile(money_regex)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
})


def get_currency_from_string(string):
    regex_result = regex.search(string)
    if regex_result:
        ret = regex_result.group()#.replace('$', '').replace('.', '')
        return ret
    string = string.split()
    ret = []
    for s in string:
        try:
            number = int(s.replace('.', ''))
            ret.append(number)
        except:
            continue
    return ret

def search_href(url):
    list_href = []
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in soup.find_all('a', href=True):
        if 'franquia-' in i['href']:
            list_href.append(i['href'])
    return list_href


def scrap_franchise(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tipo = soup.find('span', class_='badge').text

    name = soup.find('h1').text
    name = name.replace('FRANQUIA', '').strip()

    node = soup.findAll('p', class_='p-title-default my-0')

    first_time = True

    return_dict = {
        'name': name,
        'minimum_investiment': '',
        'min_return_month': '',
        'max_return_month': '',
        'state': '',
        'ftype': tipo,
        'active_unities': '',
        'contact': '',
        'loja': {},
        'quiosque': {},
    }

    for child in node:
        if 'INVESTIMENTO' in child.text:
            inv_min = child.next_element.next_element.next_element.text.strip()
            regex_result = regex.search(inv_min)
            if regex_result:
                inv_min = regex_result.group(0).replace('$', '').replace('.', '')
            else:
                inv_min = 0
            inv_min = int(inv_min)
            return_dict['minimum_investiment'] = inv_min
            continue
        if 'RETORNO' in child.text:
            retorno = child.next_element.next_element.next_element.text.strip()
            retorno = [int(s) for s in retorno.split() if s.isdigit()]
            return_dict['min_return_month'] = min(retorno)
            return_dict['max_return_month'] = max(retorno)
            continue
        if 'SEDE' in child.text:
            sede = child.next_element.next_element.next_element.text.strip()
            return_dict['state'] = sede
            continue
        if 'UNIDADES' in child.text:
            unidades = child.next_element.next_element.next_element.text.strip()
            unidades = int(unidades)
            return_dict['active_unities'] = unidades
            continue
        if 'CONTATO' in child.text:
            contato = child.next_element.next_element.next_element.text.strip()
            return_dict['contact'] = contato
            continue

    # scrap_franchise_info(url)
    # Lojas:    btn btn-tab tab2 pb-2 carousel-cel
    # Quiosque: btn btn-tab tab2 pb-2 carousel-cel selected
    unidades_moveis = soup.find_all('div', class_='tab-content UnidadesMóveis')
    quiosques = soup.find_all('div', class_='tab-content Quiosques d-none')
    lojas = soup.find_all('div', class_='tab-content Lojas d-none')

    for key, trs in {
        'unidades_moveis': unidades_moveis.find_all('th'),
        'quiosques': quiosques.find_all('th'),
        'lojas': lojas.find_all('th')
    }.items():

        if not trs:
            continue

        for tr in trs:
            if 'capital para' in tr.text.lower():
                capital = tr.next_element.next_element.next_element.next_element.next_element
                capital = get_currency_from_string(capital.text)
                return_dict[key]['capital'] = capital
                continue
            if 'taxa de franquia' in tr.text.lower():
                taxa = tr.next_element.next_element.next_element.next_element.next_element
                taxa = get_currency_from_string(taxa.text)
                return_dict[key]['taxa'] = taxa
                continue
            if 'capital de giro' in tr.text.lower():
                giro = tr.next_element.next_element.next_element.next_element.next_element
                giro = get_currency_from_string(giro.text)
                return_dict[key]['giro'] = giro
                continue
            if 'investimento total' in tr.text.lower():
                investimento = tr.next_element.next_element.next_element.next_element.next_element
                investimento = get_currency_from_string(investimento.text)
                return_dict[key]['investimento'] = investimento
                continue

    return return_dict

# for url in urls:
#     for href in search_href(url):
#         scrap_data = scrap_franchise(href)
#         scrap_data = json.dumps(scrap_data, indent=4)
#         print(scrap_data)


def scrap_from_db():
    urls_list = Url.objects.all()

    if not urls_list:
        return False

    for url in urls_list:

        url.last_scraped = datetime.now()
        url.active = True

        href_list = search_href(url.url)

        for href in href_list:
            scrap_data = scrap_franchise(href)

            # create franchise type
            franchise_type, created = FranchiseType.objects.get_or_create(
                name=scrap_data['ftype']
            )

            # find state by name
            state, created = State.objects.get_or_create(
                name=scrap_data['state']
            )

            # create franchise
            franchise, created = Franchise.objects.get_or_create(
                name=scrap_data['name'],
                minimum_investiment=scrap_data['minimum_investiment'],
                min_return_month=scrap_data['min_return_month'],
                max_return_month=scrap_data['max_return_month'],
                state=state,
                ftype=franchise_type,
                active_unities=scrap_data['active_unities'],
                contact=scrap_data['contact'],
            )
            franchise.url_id = url.id
            franchise.save()
            url.last_scraped = datetime.now()
            print(franchise, created)

        url.active = False
        url.save()


# scrap_from_db()
