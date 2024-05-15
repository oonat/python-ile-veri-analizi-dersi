import requests
from bs4 import BeautifulSoup

class WikiScraper:
    def __init__(self, header, plimit=5):
        self.s = requests.Session()
        self.s.headers.update(header)
        self.plimit = plimit

    def scrape(self, url):
        page = self.s.get(url)
        parser = BeautifulSoup(page.text, 'html.parser')

        article_body = parser.find(class_="mw-content-ltr mw-parser-output")
        
        article_text = article_body.find_all("p")
        article_text = [p_item.text for p_item in article_text]
        article_text = "\n".join(article_text[:self.plimit])

        link_list = article_body.find_all("a", href=True)
        link_list = [a_item['href'] for a_item in link_list]
        
        return article_text, link_list