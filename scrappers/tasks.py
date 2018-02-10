from __future__ import absolute_import

import json

from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


SITE_URL = "http://www.natura.com.co"


def start_scrapping():
    page = urlopen(SITE_URL)
    soup = BeautifulSoup(page, 'html.parser')
    menus = ['perfumaria', 'corpo-e-banho', 'tratamento', 'homem', 'bebe-crianca']
    for menu in menus:
        menu_item = soup.find('div', attrs={'class': 'menu-children-menu-' + menu})
        uls = menu_item.findAll('ul', limit=1)
        for ul in uls:
            lis = ul.findAll('li', recursive=False)
            for li in lis:
                children_lists = list(li.children)
                try:
                    section_scrapping(children_lists[0]['href'])
                except Exception as e:
                    print(e)
                    pass


def section_scrapping(section):
    for page in range(100):
        html_page = urlopen(SITE_URL + section + "?page=" + str(page))
        soup = BeautifulSoup(html_page, 'html.parser')
        products = list(soup.findAll('div', attrs={'class': 'global-product'}))
        for product in products:
            href = product.find('a', attrs={'class': 'natura-part-mouseover'})['href']
            product_scrapping(href)
        if len(products) < 9:
            break


def product_scrapping(product):
    html_page = urlopen(SITE_URL + product)
    html_page = html_page.read()
    soup = BeautifulSoup(html_page, 'html.parser')
    shortlink = soup.find('link', attrs={'rel': 'shortlink'})['href']
    id_database = shortlink.split('/')[-1]
    html_page = requests.get(SITE_URL + "/product_details?!key=null&nid="+id_database+"&group=null")
    result = json.loads(html_page.content)['result']
    soup = BeautifulSoup(result, 'html.parser')
    name = soup.find('h2', attrs={'class': 'product-details-content-info-title'}).text
    code = soup.find('span', attrs={'class': 'product-details-content-info-cod'}).text
    print(name + ": " + code)
