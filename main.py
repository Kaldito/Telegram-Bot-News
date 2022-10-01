from bs4 import BeautifulSoup
import requests
from decouple import config


# -------------------------- CONSTANTS -------------------------- #
CHAT_ID = config('CHAT_ID')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
HACKER_NEWS_LINK = "https://news.ycombinator.com"
FANTASY_LINK = "https://caballerodelarbolsonriente.blogspot.com"


# -------------------------- HACKER NEWS -------------------------- #
def hacker_news():
    response = requests.get(HACKER_NEWS_LINK)
    yc_web_page = response.text

    soup = BeautifulSoup(yc_web_page, "html.parser")

    article_spans = soup.find_all(name="span", class_="titleline")
    article_tags = [span.a for span in article_spans]
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


# -------------------------- FANTASY -------------------------- #
def fantasy_news():
    response = requests.get(FANTASY_LINK)
    fantasy_web_page = response.text

    soup = BeautifulSoup(fantasy_web_page, "html.parser")

    note = soup.find(name="h3", class_="entry-title")
    note_text = note.get_text()
    note_link = note.find(name="a").get("href")

    parameters = {
        "chat_id": int(CHAT_ID),
        "text": "EL CABALLERO DEL ARBOL SONRIENTE \n\n"
                f"{note_text}. \n"
                f"{note_link}"
    }

    try:
        with open("./last_note.txt", "r") as data_file:
            data = data_file.readline()
    except FileNotFoundError:
        with open("last_note.txt", "w") as data_file:
            data_file.write(note_link)

        response = requests.post(url=TELEGRAM_API, params=parameters)
        response.raise_for_status()
        print(f"Request Status: {response.json()}\n")
    else:
        if note_link != data:
            data = note_link
            with open("last_note.txt", "w") as data_file:
                data_file.write(data)

            response = requests.post(url=TELEGRAM_API, params=parameters)
            response.raise_for_status()
            print(f"Request Status: {response.json()}\n")


# -------------------------- PROGRAM -------------------------- #
hacker_news()
fantasy_news()
