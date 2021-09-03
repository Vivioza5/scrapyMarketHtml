import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import scrapy
from cleaning import clean_price, clean_descr
from lxml import html
class MarketscrapySpider(scrapy.Spider):
    name = 'marketscrapy'
    allowed_domains = ['pn.com.ua']
    start_urls = ['https://pn.com.ua/ct/2156/?ff=5113']
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}
    url='https://pn.com.ua/'


    def parse(self, response):

        for item_div in response.xpath('//article[@class="item td-table"]'):
                link=item_div.xpath('./descendant::div[@class="catalog-block-head"]/a')
                href=link.xpath('./@href').get()
                title=link.xpath('./text()').get()
                img_urls=item_div.xpath('./descendant::img[@class="photo"]/@src').get()
                raw_price=item_div.xpath('./descendant::a[@class="price"]/span/strong/text()').get()
                price = raw_price and clean_price(raw_price) or None
                descr=item_div.xpath('./descendant::a[@class="description"]').get()
                descript= re.sub('<[^<]+?>', '',descr)


                yield{
                    'title':title,
                    'href':response.urljoin(href),
                    'imgs': img_urls,
                    'price':price,
                    'descr':descript

                }
                # next_page_url =response.css("li.page-next > a::attr(href)").extract_first()
                # if next_page_url is not None:
                #     yield scrapy.Request(response.urljoin(next_page_url))



