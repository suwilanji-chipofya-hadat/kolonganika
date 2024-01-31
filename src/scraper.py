import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self, base_urls):
        self.base_urls = base_urls
        self.data = []

        self.run()
    def run(self):
        for url in self.base_urls:
            r = requests.get(url)
            if r.status_code == 200:
                s = BeautifulSoup(r.content, "lxml-xml")
                self.parse(s)
            else:
                raise Exception(f"Cannot query url: {url}")
    
    def parse(self,s):
        type_ =s.find().name
        if type_ == "sitemapindex":
            for idx in s.find_all("sitemap"):
                r = requests.get(idx.loc.text)
                if r.status_code == 200:
                    a = BeautifulSoup(r.content, "lxml-xml")
                    self.parse(a)
                else:
                    raise Exception(f"Cannot query url: {idx.loc.text}")
        elif type_ == "urlset":
            for d in s.find_all("url"):
                url_data = {}
                for property_ in d.children:
                    if property_.name == "image":
                        url_data[property_.name] = property_.loc.text
                    else:
                        url_data[property_.name] = property_.text
                self.data.append(url_data)
