import requests
import category_crawler as cc
import sys
import csv
from bs4 import BeautifulSoup

website = 'http://books.toscrape.com/
productUrls = []

def crawlPages(url):
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print(e)
    return False
  bs = BeautifulSoup(r.content, 'html.parser')
  return bs

def getCategoryLinks():
  categoryLinks = []
  for category in bs.select('ul.nav-list ul li a'):
    categoryLinks.append(category['href'])
  return categoryLinks

def browseCategories(baseUrl, pageLink):
  bs = crawlPages(f'{baseUrl}{pageLink}')
  getProductUrls(bs)
  try:
    nextPage = bs.find('li', class_='next').a['href']
  except AttributeError:
    pass
  else:
    browseCategory(baseUrl, nextPage)

def getProductUrls(bs):
  products = bs.find_all('article', class_='product_pod')
  for article in products:
    productLink = article.h3.a['href']
    productUrls.append(f'http://books.toscrape.com/catalogue/{productLink[9:]}')

bs = crawlPages(f'{website}index.html')
categoryLinks = getCategoryLinks()

for link in categoryLinks:
  browseCategories(link.replace('index.html', ''), 'index.html')

for link in productUrls:
  bs = crawlPages(link)
  data_dict = extractProductData(bs)
  saveDataToFile(data_dict)


while cc.checkInEntries(categories):

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

filePath = f"./data/{productData['Category']}.csv"
headers = productData.keys()
items = productData.values()
with open(filePath, 'w+') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(headers)
  writer.writerow(items)

