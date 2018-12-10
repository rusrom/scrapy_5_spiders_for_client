# -*- coding: utf-8 -*-
import scrapy
import json
import csv

from openpyxl import Workbook


def pager(page):
    return str(page).zfill(5)


class CountryfinancialSpider(scrapy.Spider):
    name = 'countryfinancial'
    allowed_domains = ['countryfinancial.com']

    def start_requests(self):
        url_template = 'https://www.countryfinancial.com/services/generic-forms?configNodePath=%2Fcontent%2Fcfin%2Fen%2Fjcr%3Acontent%2FrepLocator&repSearchType=location&cfLang=en&repSearchValue={}'
        urls = (url_template.format(pager(i)) for i in range(1001, 99951))

        for url in urls:
            yield scrapy.Request(url)

    def parse(self, response):
        all_agents = response.xpath('//div[contains(@class, "column-two repCard")]//a[contains(text(), "Visit my site")]/@href').extract()

        if all_agents:
            for agent_page in all_agents:
                yield scrapy.Request(url=agent_page + '/', callback=self.parse_agent)

    def parse_agent(self, response):
        agent_data = {}

        script = response.xpath('//script[contains(text(), "window.JSContext")]/text()').extract_first().strip()
        prepare_to_json = script.strip().lstrip('window.JSContext = ').rstrip(';')

        data = json.loads(prepare_to_json)

        agent_data['First Name'] = data['profile'].get('first_name', "")

        middle = data['profile'].get('middle_name', "")
        last = data['profile'].get('last_name', "")
        agent_data['Last Name'] = middle + ' ' + last if middle else last

        street = data['profile']['address'].get('street', "")
        suite = data['profile']['address'].get('suite', "")
        agent_data['Address'] = street + ' ' + suite if suite else street

        agent_data['City'] = data['profile']['address'].get('city', "")
        agent_data['State'] = data['profile']['address'].get('state', "")
        agent_data['ZIP'] = data['profile']['address'].get('zip_code', "")
        agent_data['Office Phone'] = data['profile']['phones'].get('phone', "")
        agent_data['Cell Phone'] = data['profile']['phones'].get('cell', "")
        agent_data['Email'] = data['profile'].get('email', "")

        network = data['profile'].get('networks', "")
        if network:
            agent_data['LinkedIn'] = data['profile']['networks'].get('linkedin_url', "")
            agent_data['Facebook'] = data['profile']['networks'].get('facebook_url', "")

        agent_data['Link to Site'] = data.get('base_link', "")

        yield agent_data

    def close(self, reason):
        wb = Workbook()
        ws = wb.active

        with open('country_financial.csv') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save('country_financial.xlsx')
