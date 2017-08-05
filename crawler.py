# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup


alphabet = [
    'A','B','C','D','E','F',
    'G','H','I','J','K','L',
    'M','N','O','P','Q','R',
    'S','T','U','V','W','X',
    'Y','Z']

url = "http://www.dicionáriomédico.com/A"

# https://spores.slack.com/


def equal_all_list(list_term):

    """
    Função que preencha com None as listas menores até o chegar no tamanho da maior. 
    :param list_term: 
    :return: 
    """

    high = int(0)

    # Descobre o maior
    for l in list_term:
        if len(l) > high:
            high = len(l)

    #Preenche com None
    for l in list_term:
        num_letter = len(l)
        if num_letter < high:
            for i in range(high-num_letter):
                l.append(None)
    return list_term


def next_page_by_proximo(soup):
    """
    Retorna um link para a proxima pagina
    """
    next_page = soup.find('li', {'class': 'next_btn'}).find('a')
    return next_page['href']


def next_page_by_letter(soup):
    """
    Retorna uma lista de paginas, "/A/pagina2.html"
    """
    next_page = soup.find_all('ul', {'class': 'letter_page_nav'})
    pages = [a['href'] for a in next_page[1].find_all('a')]
    return pages


def list_of_terms_medical_by_page(soup):

    """
    Return a list of terms by page for letter
    """

    result = soup.find('table', {'align': 'center'})
    result2 = [a.string for a in result.find_all('a')]
    return result2


def write_list_terms_of_csv(list_term):
    list_term = equal_all_list(list_term)
    with open("list_terms.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)

        list_term = zip(*list_term)
        for data in list_term:
            writer.writerow(data)


def crawler():

    dic_term = []
    list_terms_by_letter = []
    html_text = None
    url_alphabet = "http://www.dicionáriomédico.com/{0}"

    for letter in alphabet:

        try:
            html_text = requests.get(url_alphabet.format(letter))
        except requests.exceptions.RequestException as e:
            print(e)

        soup = BeautifulSoup(html_text.content, 'html.parser')
        print(url_alphabet.format(letter))

        pages = next_page_by_letter(soup)

        for p in pages:

            try:
                html_text = requests.get(url_alphabet.format(p))
            except requests.exceptions.RequestException as e:
                return e

            soup = BeautifulSoup(html_text.content, 'html.parser')
            lista_termos = list_of_terms_medical_by_page(soup)
            print(p)
            dic_term += lista_termos

        print(dic_term)
        list_terms_by_letter.append(dic_term)
        dic_term = []
    equal_all_list(list_terms_by_letter)
    return list_terms_by_letter


def main():
    a = crawler()
    write_list_terms_of_csv(a)
    print(a)

if __name__ == "__main__":
    main()