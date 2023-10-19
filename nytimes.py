import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_and_print_content(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract and print the content (modify selectors accordingly based on the website's structure)

            article_header = soup.find(
                'div', class_='article-header').find('header').text.strip()

            paragraphs = soup.find_all(
                'div', class_='article-paragraph')
            content = []
            for p in paragraphs:
                if p.find('figure'):
                    continue
                content.append(p.text.strip())

            # images=soup.find_all("img",{'data-lazyload':re.compile(".*")})
            print("Title:", article_header)
            print("Content:", "\n\n".join(content))
           # for img in images:
            # print(img['data-lazyload'])

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
        li_elements = soup.find_all(
            'li', {'data-tb-region-item': re.compile('.*')})

        for li in li_elements:

            link = li.find('a')
            href = urljoin(url, link['href'])

            if link:
                parse_and_print_content(href)
    except requests.exceptions.RequestException as e:
        print("Error:", e)


# Example usage
start_url = 'https://cn.nytimes.com/'
parse_news(start_url)
