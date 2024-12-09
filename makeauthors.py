import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from tqdm import tqdm
import orjson

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
author_ids = set()
links = [
    'https://www.goodreads.com/list/show/143500',
    "https://www.goodreads.com/list/show/4093",
    "https://www.goodreads.com/list/show/5",
    "https://www.goodreads.com/list/show/17",
    "https://www.goodreads.com/list/show/9",
    "https://www.goodreads.com/list/show/21",
    "https://www.goodreads.com/list/show/18",
    "https://www.goodreads.com/list/show/22",
    "https://www.goodreads.com/list/show/23",
    "https://www.goodreads.com/list/show/85",
    "https://www.goodreads.com/list/show/39%22",
    "https://www.goodreads.com/list/show/93",
    "https://www.goodreads.com/list/show/38",
    "https://www.goodreads.com/list/show/1386",
    "https://www.goodreads.com/list/show/2457",
    "https://www.goodreads.com/list/show/2594",
    "https://www.goodreads.com/list/show/2458",
    "https://www.goodreads.com/list/show/2592",
    "https://www.goodreads.com/list/show/2588",
    "https://www.goodreads.com/list/show/2591",
    "https://www.goodreads.com/list/show/2593",
    "https://www.goodreads.com/list/show/25498",
    "https://www.goodreads.com/list/show/4375"
]

def get_book_authors_on_page(link, page_count=1, timeout=10):
    try:
        # Attempt to fetch the page with a specified timeout
        page = requests.get(f"{link}?page={page_count}", headers=headers, timeout=timeout)
        page.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the page content
        pageParsed = BeautifulSoup(page.content, 'lxml')
        books = pageParsed.find('table')
        if not books:  # Handle cases where the table is not found
            print(f"No book table found on page {page_count}.")
            return []

        books = books.find_all('tr')
        local_author_ids = set()
        for book_ele in books:
            link = book_ele.find('a', {'class': 'authorName'})
            if link is None:
                continue
            author_id = link['href'].split('/')[-1]
            local_author_ids.add(author_id)

        ret = list(local_author_ids)
        print("Got", len(ret), "authors on page", page_count)
        return ret
    except requests.exceptions.RequestException as e:
        # Catch any request-related exceptions
        print(f"Request error on page {page_count}: {e}")
    except Exception as e:
        # Catch all other exceptions
        print(f"An error occurred on page {page_count}: {e}")

    # Return an empty array in case of an error
    return []

for link in tqdm(links):

  page_count = 1;
  books = get_book_authors_on_page(link, page_count)

  while len(books) > 0:
    for author_id in books:
      author_ids.add(author_id)

    page_count += 1
    books = get_book_authors_on_page(link, page_count)

    with open('authorids.json', 'wb') as file:
        file.write(orjson.dumps(list(author_ids), option=orjson.OPT_INDENT_2))

author_ids = list(author_ids)

with open('authorids.json', 'wb') as file:
  file.write(orjson.dumps(list(author_ids), option=orjson.OPT_INDENT_2))

print("Data saved to authorids.json")
print(len(author_ids), list(author_ids)[:10])
