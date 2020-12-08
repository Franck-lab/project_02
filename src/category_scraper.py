import requests
import csv
from bs4 import BeautifulSoup

baseUrl = 'http://books.toscrape.com/catalogue/category/books/fiction_10/'

def browseCategory(baseUrl, pageLink):
  r = requests.get(f'{baseUrl}{pageLink}')
  bs = BeautifulSoup(r.content, 'html.parser')
  getProductUrl(bs)
  try:
    nextPage = bs.find('li', class_='next').a['href']
  except AttributeError:
    pass
  else:
    browseCategory(baseUrl, nextPage)

def getProductUrl(bs):
  products = bs.find_all('article', class_='product_pod')
  for article in products:
    productLink = article.h3.a['href']
    print(f'http://books.toscrape.com/catalogue/{productLink[9:]}')

browseCategory(baseUrl, 'index.html')
