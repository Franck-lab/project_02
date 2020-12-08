import requests
import csv
from bs4 import BeautifulSoup

website = 'http://books.toscrape.com/'
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
    browseCategories(baseUrl, nextPage)

def getProductUrls(bs):
  products = bs.find_all('article', class_='product_pod')
  for article in products:
    productLink = article.h3.a['href']
    productUrls.append(f'http://books.toscrape.com/catalogue/{productLink[9:]}')

bs = crawlPages(f'{website}index.html')
categoryLinks = getCategoryLinks()

for link in categoryLinks:
  link = f"{website}{link.replace('index.html', '')}"
  browseCategories(link, 'index.html')


def getTitle(bs):
  try:
    title = bs.find('div', class_='product_main').h1.get_text()
  except AttributeError:
    print('This page is missing something! Skipping...')
    title = ''
  return title


def getImageUrl(bs):
  try:
    imgLink = bs.find('div', class_='carousel-inner').img['src']
    imgUrl = 'http://books.toscrape.com' + imgLink[5:]
  except AttributeError:
    print('This page is missing something! Skipping...')
    imgUrl = ''
  return imgUrl


def getProductDescription(bs):
  try:
    desc = bs.find('article', class_='product_page').find('p', recursive=False).get_text()
  except AttributeError:
    print('This page is missing something! Skipping...')
    desc = ''
  return desc


def extractProductData(bs):
  extractedData = {}
  extractedData['title'] = getTitle(bs)
  extractedData['image url'] = getImageUrl(bs)
  extractedData['product description'] = getProductDescription(bs)
  category = bs.find('ul', class_='breadcrumb').select('li:nth-of-type(3)')[0].a
  extractedData['category'] = category.get_text()
  tableRows = bs.select('table.table-striped tr')
  extractedData['upc'] = tableRows[0].td.text
  extractedData['price excluding tax'] = tableRows[2].td.text
  extractedData['price including tax'] = tableRows[3].td.text
  extractedData['number available'] = tableRows[5].td.text
  extractedData['review rating'] = tableRows[6].td.text
  return extractedData


def saveDataToFile(data_dict, header=False):
  filePath = f"./data/{data_dict['category'].lower()}.csv"
  with open(filePath, 'a') as f:
    fieldnames = data_dict.keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not header:
      writer.writeheader()
    writer.writerow(data_dict)

filenames = []
for link in productUrls:
  bs = crawlPages(link)
  data_dict = extractProductData(bs)
  data_dict['product url'] = link
  if data_dict['category'].lower() in filenames:
    saveDataToFile(data_dict, header=True)
  else:
    saveDataToFile(data_dict, header=False)
    filenames.append(data_dict['category'].lower())
  # downloadProductImage(data_dict['image url'])



