import requests
import csv
from bs4 import BeautifulSoup

# def scrapeP
#
# def browseCategory(currentPage, )

r = requests.get('http://books.toscrape.com/catalogue/category/books/fiction_10/index.html')
bs = BeautifulSoup(r.content, 'html.parser')

productTags = bs.find_all('article', class_='product_pod')
for article in productTags:
  productLink = article.h3.a['href']
  print(f'http://books.toscrape.com/catalogue/{productLink[9:]}')
