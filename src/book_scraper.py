import requests
from bs4 import BeautifulSoup

reponse = requests.get('http://books.toscrape.com/catalogue/soumission_998/index.html')
html = reponse.content
bs = BeautifulSoup(html, 'html.parser')

productData = {}

productData['url'] = reponse.url
productData['title'] = bs.find('div', class_='product_main').h1.get_text()
imgTag = bs.find('div', class_='carousel-inner').img
productData['image url'] = imgTag.attrs['src']
productData['image url'] = 'http://books.toscrape.com' + productData['image url'][5:]
productData['product description'] = pTag = bs.find('article', class_='product_page').find('p', recursive=False).get_text()
category = bs.find('ul', class_='breadcrumb').select('li:nth-of-type(3)')[0].a
productData['category'] = category.get_text()
tableRows = bs.find('table', class_='table-striped').find_all('tr')


for row in tableRows:
  productData[row.th.get_text()] = row.td.get_text()

for key, value in productData.items():
  print(f'{key}:\t{value}')
