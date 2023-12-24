import requests
import re
from bs4 import BeautifulSoup

from flask_app import app, db
from flask_app.models import News
with app.app_context():
    db.create_all()
    link = 'https://www.wowhead.com/news?type=1'
    response = requests.get(link)

    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.find_all(href=re.compile("news"))

    count = 1
    for item in news:
        item = str(item)
        if '<a href="/news/' in item and count < 6:
            split_link = item.split('>', 1)
            split_link[0] = split_link[0].replace('<a href="/news/', '<a href="https://www.wowhead.com/news/')
            new_link = split_link[0] + ' target="#">' + split_link[1]
            current_data = News.query.filter(News.id == count).first()
            current_data.anchor = new_link
            try:
                print("Commiting to the db...")
                db.session.commit()
                print(f"I commited {current_data} to the db")
            except:
                print('There was an issue writting to the db :(')

            count = count + 1