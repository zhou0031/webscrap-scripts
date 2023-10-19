import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import Counter


def parse_and_print_content(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract and print the content (modify selectors accordingly based on the website's structure)
            title = soup.find('h1').text.strip()
            ps = soup.find(class_=re.compile(
                "index_main_content.*")).find_all("p", class_="")
            content = []
            for p in ps:
                content.append(p.text.strip())
            images = soup.find_all("img", {'data-lazyload': re.compile(".*")})

            imgs = []
            for image in images:
                imgs.append(image['data-lazyload'])
            print("Title:", title)
            print("Content:", "\n\n".join(content))
            print("Images:\n", "\n\n".join(imgs))

            print("-" * 30)
        else:
            print("Failed to retrieve the page:", link)
    except requests.exceptions.RequestException as e:
        print("Error:", e)


def parse_news(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page: {url}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all h3 elements
        h2_elements = soup.find_all('h2')

        for h2 in h2_elements:
            link = h2.find('a')
            href = urljoin(url, link['href'])

            if link:
                parse_and_print_content(href)
    except requests.exceptions.RequestException as e:
        print("Error:", e)


# Example usage
start_url = 'https://news.ifeng.com/'
parse_news(start_url)
