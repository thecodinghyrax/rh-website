import requests
import re
from bs4 import BeautifulSoup
from flask_app import db
from flask_app.models import News

link = 'https://www.wowhead.com/news'
response = requests.get(link)

soup = BeautifulSoup(response.text, "html.parser")
news = soup.find_all(href=re.compile("news="))

count = 1
for item in news:
    item = str(item)
    if "<a href" in item and count < 6:
        split_link = item.split('>', 1)
        new_link = split_link[0] + ' target="#">' + split_link[1]
        current_data = db.session.query(News).filter_by(id = count).first()
        current_data.anchor = new_link
        try:
            db.session.commit()
        except:
            print('There was an issue writting to the db :(')
        count = count + 1

