# -*- coding: utf-8 -*-
import scrapy
import re
import csv

from selenium import webdriver
from scrapy.selector import Selector
from time import sleep
from random import randint


class TruckpaperTrucksSpider(scrapy.Spider):
    name = 'truckpaper-trucks'
    # allowed_domains = ['truckpaper.com']
    allowed_domains = ['machinerytrader.com']
    
    # start_urls = ['https://www.truckpaper.com/listings/trucks/for-sale/category/27/trucks']

    def start_requests(self):
        
        # self.driver = webdriver.Chrome('/home/rusrom/webdrivers/chromedriver')
        # # self.driver.get('https://www.truckpaper.com/listings/trucks/for-sale/category/27/trucks')
        # self.driver.get('https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment')
        # sleep(8)
        # sel = Selector(text=self.driver.page_source)
        # self.driver.close()

        # with open('machinerytrader.csv', 'a', encoding='utf-8') as f_csv:
        #     fieldnames = ['make', 'model']
        #     csv_writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        #     csv_writer.writeheader()

        # makers = sel.xpath('//div[@class="column12 fluid-mobile columns large-12 medium-12 small-12"]/div[@class="p-bottom-30 p-top-5 listings-drilldown cf row"]//li/a[contains(@href, "for-sale/category")]/@href').extract()
        makers = [
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/still',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/stone',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/sullair',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/sullivan',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/sullivan-palatek',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/sumitomo',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/sunward',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/superior',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/superior-broom',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/symons',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tadano',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/takeuchi',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tamrock',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/taylor',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/taylor-dunn',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tcm',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/telelect',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/telestack',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/telsmith',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tennant',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/terex',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/terex-finlay',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/terex-pegson',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/terramite',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tesab',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tesmec',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/texoma',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/thomas',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/thompson',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/thwaites',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tigercat',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/timbco',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/timberjack',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/timberpro',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/toro',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tower-light',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/toyota',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/trackmobile',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/trio',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/tymco',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/unic',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/unicarriers',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/unitedbuilt',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/universal',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/up-right',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/utilev',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/valmet',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/venieri',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/vermeer',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/versalift',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/vibromax',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/viper',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/vogele',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/volvo',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/wabco',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/wacker',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/wacker-neuson',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/wagner',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/waukesha',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/weber',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/weiler',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/white-lai',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/wirtgen',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/woods',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/xcmg',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/xtreme-mfg',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/yale',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/yamaha',
            'https://www.machinerytrader.com/listings/construction-equipment/for-sale/category/4/construction-equipment/manufacturer/yanmar',
        ]
        
        # (2) -> Open 1 instanse and just go through pages
        # self.driver = webdriver.Chrome('/home/rusrom/webdrivers/chromedriver')
        for make in makers:
            with open('machinerytrader.csv', 'a', encoding='utf-8') as f_csv:
                fieldnames = ['make', 'model']
                csv_writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
                vendor = make.split('/')[-1].title()

                # (1) -> Always open new browser instance on maker
                self.driver = webdriver.Chrome('/home/rusrom/webdrivers/chromedriver')
                # self.driver.get('https://www.truckpaper.com' + make)
                self.driver.get(make)

                sleep(randint(10, 30))
                sel = Selector(text=self.driver.page_source)
                # (1) -> Always close instance for each page
                self.driver.close()

                models = sel.xpath('(//div[@class="column12 fluid-mobile columns large-12 medium-12 small-12"]/div[@class="p-bottom-30 p-top-5 listings-drilldown cf row"]/div/ul/li[not(@class)] | //div[@class="column12 fluid-mobile columns large-12 medium-12 small-12"]/div[@class="p-bottom-30 p-top-5 listings-drilldown cf row"]/div/ul/li[@class="with-children"]/ul[@class="closed"]/li)/a/text()').extract()
                for model in models:
                    data = {}
                    data['make'] = vendor
                    data['model'] = re.sub(r'\s+\(\d+\)', '', model).strip()
                    print(data)
                    csv_writer.writerow(data)
            # (2) -> Close instance after complete through all makers
            # self.driver.close()
