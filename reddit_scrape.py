import re
import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import http.client, urllib.parse

def scrape_reddit():
    url = "https://old.reddit.com/r/datascience/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    r1 = requests.get(url, headers = headers)
    counter = 1
    df = pd.DataFrame()
    titles = []
    authors = []
    total_comments = []
    total_likes = []
    soup = BeautifulSoup(r1.content, "html.parser")

    attrs = {'class': 'thing', 'data-domain': 'self.datascience'}
    while (counter <= 10):
        posts = soup.find_all('div', attrs=attrs)
        for post in posts:
            titles.append(post.find('p', class_="title").text)
            authors.append(post.find('a', class_='author').text)
            comments = post.find('a', class_='comments').text.split()[0]
            if comments == "comment":
                comments = 0
            total_comments.append(comments)
            likes = post.find("div", attrs={"class": "score likes"}).text
            if likes == "•":
                likes = "None"
            total_likes.append(likes)
        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        counter+=1

    df['Titles'] = titles
    df['Authors'] = authors
    df['Comments'] = total_comments
    df['Likes'] = total_likes

    df.to_csv('reddit_data_science.csv',header=True)
    return df

scrape_reddit()