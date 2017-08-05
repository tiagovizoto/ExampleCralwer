import requests
import re
from bs4 import BeautifulSoup

def main():
    url = "http://www.dicionáriomédico.com/A"

    text = requests.get(url).text

    soup = BeautifulSoup(text, 'html.parser')

    print(soup.prettify())

    for link in soup.find_all('a'):
        print(link.get('href'))



if "__main__" == __name__:
    main()
