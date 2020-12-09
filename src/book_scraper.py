import requests
import csv
from bs4 import BeautifulSoup


def crawlPages(url):
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print(e)
    return False
  bs = BeautifulSoup(r.content, 'html.parser')
  return bs


def getCategoryLinks(homePageBS):
  categoryLinks = []
  for category in homePageBS.select('ul.nav-list ul li a'):
    categoryLinks.append(category['href'])
  return categoryLinks


def browseCategories(baseUrl, pageLink, productUrls):
  categoryBS = crawlPages(f'{baseUrl}{pageLink}')
  productUrls.extend(getProductUrls(categoryBS))
  try:
    nextPage = categoryBS.find('li', class_='next').a['href']
  except AttributeError:
    pass
  else:
    productUrls = browseCategories(baseUrl, nextPage, productUrls)
  return productUrls


def getProductUrls(categoryBS):
  baseUrl = 'http://books.toscrape.com/catalogue/'
  products = categoryBS.find_all('article', class_='product_pod')
  productUrls = []
  for article in products:
    productLink = article.h3.a['href']
    productUrls.append(f'{baseUrl}{productLink[9:]}')
  return productUrls


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


def extractProductData(productPageBS):
  extractedData = {}
  extractedData['title'] = getTitle(productPageBS)
  extractedData['image url'] = getImageUrl(productPageBS)
  extractedData['product description'] = getProductDescription(productPageBS)
  category = productPageBS.find('ul', class_='breadcrumb').select('li:nth-of-type(3)')[0].a
  extractedData['category'] = category.get_text()
  tableRows = productPageBS.select('table.table-striped tr')
  extractedData['upc'] = tableRows[0].td.text
  extractedData['price excluding tax'] = tableRows[2].td.text
  extractedData['price including tax'] = tableRows[3].td.text
  extractedData['number available'] = tableRows[5].td.text
  extractedData['review rating'] = tableRows[6].td.text
  return extractedData


def saveDataToFile(data_dict):
  header = data_dict.pop('header', False)
  filePath = f"./data/{data_dict['category'].lower()}.csv"
  with open(filePath, 'a') as f:
    fieldnames = data_dict.keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not header:
      writer.writeheader()
    writer.writerow(data_dict)


def main():
  website = 'http://books.toscrape.com/'
  productUrls = []
  homePageBS = crawlPages(f'{website}index.html')
  categoryLinks = getCategoryLinks(homePageBS)
  filenames = []
  for link in categoryLinks:
    link = f"{website}{link.replace('index.html', '')}"
    productUrls = browseCategories(link, 'index.html', productUrls)
    for link in productUrls:
      productPageBS = crawlPages(link)
      data_dict = extractProductData(productPageBS)
      data_dict['product url'] = link
      if data_dict['category'].lower() in filenames:
        data_dict['header'] = True
        saveDataToFile(data_dict)
      else:
        data_dict['header'] = False
        saveDataToFile(data_dict)
        filenames.append(data_dict['category'].lower())
    productUrls = []


main()
