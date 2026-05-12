import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import json

url_base = 'https://www.coffeereview.com/review/page/'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'}
index_pages = []
links = []
subpages = []
pre_df = {'Roaster Name' : [], 'Rating': [], 'Review Title' : [], "Image": [], "Blind Assessment" : [],
          "Notes": [], "Bottom line":[], 'Roaster Location': [], 'Coffee Origin': [], 'Roast Level':[],
          'Agtron': [], 'Est. Price':[], 'Review Date': [], 'Aroma':[], 'Body':[], 'Flavor': [],
          'Aftertaste': [], 'With Milk':[]}

# Getting the index pages
for i in range(1, 450):
    try:
        site = requests.get(url_base + str(i), headers=headers)
    except:
        continue
    sleep(1)
    index_pages.append(site)
    print(f"{i} / 3")

# Extracting the links to each review
for i, page in enumerate(index_pages):
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    links_div = soup.find_all('p', class_ = 'review-roaster')
    links_temp = [i.select_one('a')['href'] for i in links_div]
    links += links_temp

# Getting each review's site
for i, link in enumerate(links):
    try:
        site = requests.get(link, headers=headers)
    except:
        continue
    sleep(1)
    subpages.append(site)
    print(f"{i} / {len(links)}")

# Extracting the info from each review
for i, subpage in enumerate(subpages):
    soup = BeautifulSoup(subpage.content, 'html.parser')
    border = soup.select_one('div.review-template')
    rows = border.find_all('tr')
    name = border.select_one('p.review-roaster').text
    review = border.select_one('h1.review-title').text
    img_element = border.select_one('img')
    img = "" if img_element is None else img_element['src']
    texts = border.select_one("div[class='row row-2']").find_all_next('p') # find paragraphs after table
    rating = border.select_one("span.review-template-rating").text

    pre_df['Roaster Name'].append(name)
    pre_df['Rating'].append(rating)
    pre_df['Review Title'].append(review)
    pre_df["Image"].append(img)
    pre_df["Blind Assessment"].append(texts[0].text)
    pre_df["Notes"].append(texts[1].text)
    pre_df["Bottom line"].append(texts[2].text)

    doubles = [row.find_all('td') for row in rows]
    for pair in doubles:
        attr, val = pair[0].text.replace(':','').strip(), pair[1].text
        if attr in pre_df:
            pre_df[attr].append(val)
    should_be = len(pre_df['Roaster Name'])
    for attr in pre_df:
        if len(pre_df[attr]) < should_be:
            pre_df[attr].append(np.nan)

df = pd.DataFrame(pre_df)
df.to_csv("df.csv")

