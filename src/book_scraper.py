import requests
import csv
from bs4 import BeautifulSoup

reponse = requests.get('http://books.toscrape.com/catalogue/soumission_998/index.html')
html = reponse.content
bs = BeautifulSoup(html, 'html.parser')

productData = {}

productData['url'] = reponse.url
productData['Title'] = bs.find('div', class_='product_main').h1.get_text()
imgTag = bs.find('div', class_='carousel-inner').img
productData['Image url'] = imgTag['src']
productData['Image url'] = 'http://books.toscrape.com' + productData['Image url'][5:]
productData['Product description'] = pTag = bs.find('article', class_='product_page').find('p', recursive=False).get_text()
category = bs.find('ul', class_='breadcrumb').select('li:nth-of-type(3)')[0].a
productData['Category'] = category.get_text()
tableRows = bs.find('table', class_='table-striped').find_all('tr')


for row in tableRows:
  productData[row.th.get_text()] = row.td.get_text()

del productData['Tax']
del productData['Product Type']

filePath = './data/' + productData['Category'] + '.csv'
headers = productData.keys()
items = productData.values()
with open(filePath, 'w+') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(headers)
  writer.writerow(items)

