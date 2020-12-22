import scraper as scp

def main():
  website = 'http://books.toscrape.com/'
  productUrls = []
  homePageBS = scp.crawlPages(f'{website}index.html')
  categoryLinks = scp.getCategoryLinks(homePageBS)
  categories = []
  for link in categoryLinks:
    link = f"{website}{link.replace('index.html', '')}"
    productUrls = scp.browseCategories(link, 'index.html', productUrls)
    for link in productUrls:
      productPageBS = scp.crawlPages(link)
      data_dict = scp.extractProductData(productPageBS)
      data_dict['product url'] = link
      if data_dict['category'].lower() in categories:
        data_dict['header'] = True
        scp.saveDataToFile(data_dict)
      else:
        data_dict['header'] = False
        scp.saveDataToFile(data_dict)
        categories.append(data_dict['category'].lower())
      scp.downloadProductImage(data_dict['image url'])
    productUrls.clear()

main()