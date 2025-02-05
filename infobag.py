import requests
from bs4 import BeautifulSoup


#detalles del pedido 
url = 'https://finance.yahoo.com/quote/NVDA/'
encabezados = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}
html = requests.get(url, headers= encabezados)

#crear sopa
soup = BeautifulSoup(html.content, 'lxml')

# Extraer el elemento con el atributo data-testid específico
info_encabezado = soup.find(attrs={"data-testid": "quote-hdr"})
titulo_simbolo = info_encabezado.find('h1')
precio_actual = info_encabezado.find('span', attrs={"data-testid": "qsp-price"})

#extraer tabla
tablas = soup.find('ul', class_='yf-gn3zu3').find_all('li')

for li in tablas:
    nombre = li.find_all('span')[0].get_text()
    valor = li.find_all('span')[1].get_text()
    print(nombre + '- '+ valor)


