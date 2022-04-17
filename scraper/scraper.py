#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests


def scrapedata():
    #Retrieving and parsing HTML data
    html_data = requests.get('https://bnr.bg/lyubopitno/list').text
    soup = bs(html_data, "html.parser")
    titles = soup.find_all(itemprop='name')
    dates = soup.find_all(itemprop='datePublished')
    links = soup.find_all(itemprop='url')
    links2 = []
    for link in links:
        if link.has_attr('href'):
            links2.append(link['href'])
    links2 = list(dict.fromkeys(links2))

    contentlist = []

    for link in links2:
        html_ = requests.get(f'https://bnr.bg{link}').text
        soup_ = bs(html_, "html.parser")
        content = soup_.find_all(itemprop ='articleBody')
        for item in content:
            titem = item.get_text()
            contentlist.append(titem)

    title_date_content_list = []

    for i in range(len(dates)):
        a = titles[i].get_text()
        b = (dates[i].get_text()).strip()
        c = contentlist[i].strip()
        templist = [a, b, c]
        title_date_content_list.append(templist)

    return title_date_content_list
