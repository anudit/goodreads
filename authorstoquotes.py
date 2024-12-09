import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from tqdm import tqdm
import orjson

def extract_data_quote(quotes_html):
  quotes = []
  for quote_html in quotes_html.find_all('div', {'class': 'quote'}):
    quote = quote_html.find('div', {'class': 'quoteText'}).get_text().strip().split('\n')[0]
    author = quote_html.find('span', {'class': 'authorOrTitle'}).get_text().strip()
    if quote_html.find('div', {'class': 'greyText smallText left'}) is not None:
        tags_list = [tag.get_text() for tag in quote_html.find('div', {'class': 'greyText smallText left'}).find_all('a')]
        tags = list(OrderedDict.fromkeys(tags_list))
        if 'attributed-no-source' in tags:
            tags.remove('attributed-no-source')
    else:
        tags = None

    quotes.append({'quote': quote, 'author': author, 'tags': tags})
  return quotes

def author_id_to_quotes(id):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
  }
  all_auth_quotes = []

  page_count = 1
  page = requests.get(f"https://www.goodreads.com/author/quotes/{id}", headers=headers)
  pageParsed = BeautifulSoup(page.content, 'lxml')
  new_q = extract_data_quote(pageParsed)

  while len(new_q) > 0:
    all_auth_quotes.extend(new_q)
    page_count+=1
    # print("Getting page", page_count, id)
    page = requests.get(f"https://www.goodreads.com/author/quotes/{id}?page={page_count}", headers=headers)
    pageParsed = BeautifulSoup(page.content, 'lxml')
    new_q = extract_data_quote(pageParsed)

  return all_auth_quotes


with open("authorids.json", 'rb') as file:  # Open in binary read mode
    author_ids = orjson.loads(file.read())
print(len(author_ids))

# all_quotes = []
# for id in tqdm(author_ids):
#   all_quotes += author_id_to_quotes(id)

#   with open('quotes.json', 'wb') as file:
#     file.write(orjson.dumps(all_quotes, option=orjson.OPT_INDENT_2))
