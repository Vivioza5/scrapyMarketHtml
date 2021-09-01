#!/usr/bin/env python
from pprint import pprint
from urllib.parse import urljoin
from scrapy.spiders import Rule
# from scrapy_selenium import SeleniumRequest
import lxml
import requests
# from multiCocking.items import MulticockingItem
import re
from bs4 import BeautifulSoup, NavigableString
from scrapy.linkextractors import LinkExtractor
# from multiCocking.mymethods import OpenSearch
# import pandas as pd

import scrapy
from scrapy.loader import ItemLoader
from lxml import html
from scrapy import Request, Selector
from urllib.parse import urljoin
class SeleniumRequest(Request):
    pass
class MulticookSpider(scrapy.Spider):
    name = 'multicook'

    start_urls = ['https://pn.com.ua/']
    # allowed_domains = ['https://pn.com.ua/search/']
    # allowed_domains =['https://pn.com.ua']
    # rules = (
    #
    #     Rule(LinkExtractor(allow=('search/?page=', )), callback='parse'),
    # )
    open_url='https://pn.com.ua'
    url=None

    # querySel=OpenSearch(open_url)
    # body=querySel.open_and_entry_query()
    # title=querySel.query
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        # open page with webdriver. copy html of the page
        # querySel=OpenSearch(self.open_url)
        # body=querySel.open_and_entry_query()
        # br_selector = Selector(text = self.body)
        # print(body)
        # title=querySel.query
        # print (title)
        # print(querySel.open_link)


        name=[]
        price=[]
        description=[]
        next_page=[]
        # парсим тег и извлекаем из него текст, в случае если есть лишние теги все равно костіль потому как не получаем ключ для items пробуем разобраться с re
        html_document =self.body
        tree=html.fromstring(html_document)
        body_tags = tree.xpath('//a[@class="description"]')
        # body_tags_css=tree.css("li.next-page > a::attr(href)")
        descr=[]
        for item in body_tags:
            if item:
                body = item
                text_document = body.text_content().strip()
                descr.append(text_document)
            else:
                text_document = ''
        # pprint(descr)
        # добавление спарсеных данных в items
        l=ItemLoader(item=MulticockingItem(),selector=br_selector)
        l.add_xpath('name','//div[@class="catalog-block-head"]/a/text()')
        l.add_xpath('price','//a[@class="price"]/span/strong/text()')
        l.add_value('description',descr)
        # l.add_xpath('next_page',"descendant-or-self::li[@class and contains(concat(' ', normalize-space(@class), ' '), ' page-next ')]/a[@href]")
        l.add_css('next_page',"li.page-next > a::attr(href)")
        yield l.load_item()
        # при разніх запросах меняются локаторі віявил на материнках относится к продуктам в прайсах
        # написать раздельніе функции и проверка содержимого сайта после открітия страниці результатов поиска в зависимости от содержимого подбирать парсер
        #  не забіть сделать проверку на то что введен неправильній запрос остались вопросі по поиску відаются дубликаті в страницах результатов, без ввода поиска
        # через селениум парсинг нескольких страниц работает, но не работает вівод через пандас в таблицу смотрим pipelines
        name.extend(l.get_collected_values("name"))
        price.extend(l.get_collected_values("price"))
        description.extend(l.get_collected_values("description"))
        # print(l.get_collected_values("descr"))
        frame1 = create_frame(name,'name')
        frame2 = create_frame(description,'descr')
        frame3 = create_frame(price,'price')
        fullFrame=frame1.join(frame2).join(frame3)
        fullFrame.to_csv(f'{self.title}.csv')
        # print(price)
        next_page.extend(l.get_collected_values('next_page'))
        print('response.url',next_page)

        domain='https://pn.com.ua'
        next_page_url=br_selector.css("li.page-next > a::attr(href)").extract_first()
        cur_url=urljoin(domain,next_page_url)
        # cur_url=create_scrap_link(domain,next_page_url)
        # next_page_url =response.css("li.page-next > a::attr(href)").extract_first()

        print('concat',cur_url)

        if next_page_url is not None:
            yield response.follow(cur_url, self.parse)


# создание фрейма из списка на основе pandas
def create_frame(items, header):
        columns = []
        columns.append(header)
        # задается через параметры функции название колонки, без этого выдает нет названия у колонки
        frame = pd.DataFrame(data=items, columns=columns)

        return frame

def create_scrap_link(domain,next_page):
        curent_url=urljoin(domain,next_page)
        return curent_url
# descr=response.xpath('//a[@class="description"]/text()').get()
        # print(descr)
        # fulldescr=descr.replace('<span class="separator">•<\/span>', "")
        # fulldescr=re.sub('<span class="separator">•<\/span>', ' ',descr )
        # for res in re.findall(r'<span class="separator">(.*?)<\/span>',descr):
        #         print(res.re.sub('•', " "))
        # print(fulldescr.text())


#name= .xpath('//div[@class="catalog-block-head"]/a/text()')
# price=xpath('//a[@class="price"]')
# https://pn.com.ua/ct/2156/?ff=5113 https://pn.com.ua/ct/2156/?ff=5113&page=2
# description=xpath('//p[@class="content-item"]/a/text()').get() через цикл можно записать все в одну строку [item]
#через вебдрайвер вводить в поле поиска название продукта которій получаем из инпута урл составляем из домейнБ индекс поиска и пагинация

# def get_section_text(text, soup=None):
#     section = soup.find(text=text)
#     if not section:
#         raise ValueError("Section not found")
#
#     texts = []
#     for item in section.parent.find_next_siblings():
#         if item.name == 'strong':
#             break
#         text_before = item.previous_sibling
#         if isinstance(text_before, NavigableString):
#             texts.append(text_before)
#
#     return ' '.join(texts)
