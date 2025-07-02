import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_reddit():
    subreddit = input("Enter the subreddit name (e.g., learnpython, datascience): ").strip()
    url = f"https://old.reddit.com/r/{subreddit}/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    counter = 1
    titles, authors, total_comments, total_likes = [], [], [], []

    print(f"\nScraping subreddit: {subreddit}\n")

    while (counter <= 10):
        print(f"Scraping page {counter}...")
        r = requests.get(url, headers = headers)
        soup = BeautifulSoup(r.content, "html.parser")
        posts = soup.find_all('div', class_='thing', attrs={'data-domain': f'self.{subreddit}'})
        
        for post in posts:
            title_tag = post.find('p', class_='title')
            author_tag = post.find('a', class_='author')
            comments_tag = post.find('a', class_='comments')
            likes_tag = post.find("div", class_="score likes")
            titles.append(title_tag.text.strip() if title_tag else 'No Title')
            authors.append(author_tag.text.strip() if author_tag else 'Unknown')

            try:
                comments_text = comments_tag.text.split()[0]
                comments = int(comments_text) if comments_text.isdigit() else 0
            except:
                comments = 0
            total_comments.append(comments)
            likes = likes_tag.text if likes_tag else '0'
            total_likes.append(likes if likes.isdigit() else '0')
        # Check if there is a next page
        next_button = soup.find("span", class_="next-button")
        if not next_button:
            print("No more pages to scrape.")
            break
        url = next_button.find("a")['href']
        counter+= 1
        time.sleep(2)

    df = pd.DataFrame({
        'Title': titles,
        'Author': authors,
        'Total Comments': total_comments,
        'Total Likes': total_likes
    })
    filename = f'reddit_{subreddit}.csv'
    df.to_csv(filename, index=False)
    print(f"\nScraping completed. Data saved to {filename}\n")
    return df
scrape_reddit()