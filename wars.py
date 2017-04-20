import requests
import sys
import re
import sqlite3
import multiprocessing

conn = sqlite3.connect('database/webcrawl.db')

c = conn.cursor()

c.execute('''DROP TABLE  website;''')
c.execute('''DROP TABLE  links;''')
try:
    c.execute('''CREATE TABLE website (
                 id INT  ,
                 url VARCHAR(255) NOT NULL,
                 indexed BOOL NOT NULL DEFAULT '0',
                 PRIMARY KEY (ID) 
                 ); ''')
except:
    print 'Table: Website already exists.'
    pass

try:
    c.execute('''CREATE TABLE links (
                 id InT ,
                 url_id INT NOT NULL,
                 link_id INT NOT NULL,
                 PRIMARY KEY (id),
                 FOREIGN KEY (url_id) REFERENCES website(url),
                 FOREIGN KEY (link_id) REFERENCES website(url)
                 ); ''')
except:
    print 'Table:links already exists.'
    pass

class Website():
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        #self.domain = self.request['domain']
        #self.length = self.request['Content-Length']
        #self.content_type= self.request['Content-Type']
        self.links = []
        self.get_links()

    def get_links(self):
        self.links = re.findall('href=\"(.+?)\"', self.request.text)
        for m in self.links:
            if m[0] == "/":
                self.links.remove(m)
                self.links.append(self.url + m)


def crawling(first=True):
    while True:
        try:
            if first == False:
                url  = c.execute(''' SELECT url FROM website
                                     WHERE indexed='0' 
                                     LIMIT 1; ''')
                url = url.fetchone()[0]
                c.execute(''' UPDATE website
                              SET indexed='1'
                              WHERE url=?''',(url,))
            else:
                url = sys.argv[1]
                first = False
            site = Website(url)

            print "\033[0;31m" + url + "\033[0m"
            print len(site.links)
            for lnk in site.links:
                redun = c.execute('SELECT url FROM website WHERE url=?',(lnk, ))
                redun_url = redun.fetchone()
                if not redun_url:
                    c.execute("INSERT INTO website(url) VALUES(?)",(lnk,))
                    conn.commit()

        except KeyboardInterrupt:
            conn.close()
            quit(1)

        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidSchema:
            pass

for i in range(10):
    if i == 1:
        p = multiprocessing.Process(target=crawling)
        p.start()
    else:
        p = multiprocessing.Process(target=crawling, args=(False,))
        p.start()
