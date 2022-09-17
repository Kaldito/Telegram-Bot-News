import decouple as decouple
from bs4 import BeautifulSoup
import requests
from decouple import config


CHAT_ID = config('CHAT_ID')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

response = requests.get("https://news.ycombinator.com")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

article_tags = soup.find_all(name="a", class_="titlelink")
score_tags = soup.find_all(name="span", class_="score")
article_texts = []
article_links = []

for tag in article_tags:
    text = tag.get_text()
    link = tag.get("href")
    article_texts.append(text)
    article_links.append(link)

votes = [int(score.get_text().split()[0]) for score in score_tags]
best_article = max(votes)
i_best_article = votes.index(best_article)

parameters = {
    "chat_id": int(CHAT_ID),
    "text": "HACKER NEWS \n\n"
            f"{article_texts[i_best_article]}. \n"
            f"{article_links[i_best_article]}"
}

response = requests.post(url=TELEGRAM_API, params=parameters)
response.raise_for_status()
print(f"Request Status: {response.json()}\n")


