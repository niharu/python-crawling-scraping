import re
import sqlite3
import urllib
from urllib.request import urlopen
from html import unescape

def main():
    html = fetch('https://gihyo.jp/dp')
    books = scrape(html)
    save('books.db', books)

def fetch(url):
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
            }

    request =  urllib.request.Request(url, headers=headers)
    f = urlopen(request)
    encoding = f.info().get_content_charset(failobj="utf-8")
    html = f.read().decode(encoding)

    return html

def scrape(html):
    books = []
    for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):

        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        url = 'https://gihyo.jp' + url

        title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
        title = title.replace('<br/>', ' ')
        title = re.sub(r'<.*?>', '', title)
        title = unescape(title)

        books.append({'url':url, 'title':title})

    return books

def save(db_path, books):
    conn = sqlite3.connect(db_path)
    
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS books')

    c.execute('''
        CREATE TABLE books (
            title text,
            url text
        )
    ''')

    c.executemany('INSERT INTO books VALUES (:title, :url)', books)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
