#!/usr/bin/env python
from time import sleep
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import PySimpleGUI as sg
from tkinter import *
class MulticookSpider(scrapy.Spider):


    name = 'multicookselen'
    start_urls = ['https://pn.com.ua/']
    allowed_domains =['https://pn.com.ua']
    open_url='https://pn.com.ua'
    url=None
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response ):


        sg.theme('Default1')   # Add a touch of color
             # All the stuff inside your window.
        self.layout = [
                        [sg.Text('Please enter Query',size=(25, 1))],
                        [sg.Text('Your query', size=(10, 1)), sg.InputText()],
                        [sg.Submit(), sg.Cancel()]
        ]

        # Create the Window
        self.window = sg.Window('Window Title', self.layout)
        # Event Loop to process "events" and get the "values" of the inputs

        self.event, self.values = self.window.read()
        self.welcome =self.values[0]

        self.window.close()




        # self.welcome=QueryInputDialog.get_input_query


        self.driver= webdriver.Chrome()
        self.driver.get(response.url)
        input=self.driver.find_element_by_xpath('//*[@class="search-text-input"]')
        button=self.driver.find_element_by_xpath('//*[@class="search-group-submit"]/input')
        input.send_keys(self.welcome)
        sleep (3)
        button.click()
        sleep(3)
        sel = Selector(text=self.driver.page_source)
        print (sel.xpath('//title/text()').get())
        sleep(3)
        product=sel.xpath('//article[@class="item td-table"]')
        for item_div in product:
               link=item_div.xpath('./descendant::div[@class="catalog-block-head"]/a')
               href=link.xpath('./@href').get()
               title=link.xpath('./text()').get()
               img_urls=item_div.xpath('./descendant::img[@class="photo"]/@src').get()
               price=item_div.xpath('./descendant::a[@class="price"]/span/strong/text()').get()
               # price = raw_price and clean_price(raw_price) or None
               descr=item_div.xpath('./descendant::a[@class="description"]').get()
               descript= re.sub('<[^<]+?>', '',descr)


               yield{
                    'title':title,
                    'href':response.urljoin(href),
                    'imgs': img_urls,
                    'price':price,
                    'descr':descript

                }









