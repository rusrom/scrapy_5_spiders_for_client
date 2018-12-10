# -*- coding: utf-8 -*-
import scrapy
import csv
from openpyxl import Workbook


class StatefarmSpider(scrapy.Spider):
    name = 'statefarm'
    allowed_domains = ['statefarm.com']
    start_urls = ['https://www.statefarm.com/agent/US/']

    def parse(self, response):
        all_states = response.xpath('//div[@id="stateListUS"]//ul/li//a')
        for state in all_states:
            yield response.follow(state, callback=self.parse_cities)

    def parse_cities(self, response):
        all_cities = response.xpath('//div[@id="cityColumnOne"]//li//a')
        for city in all_cities:
            yield response.follow(city, callback=self.parse_agents)

    def parse_agents(self, response):
        agents = response.xpath('//div[@class="row-fluid agentDetailsAddress"]')
        for agent in agents:
            agent_data = {}

            name = agent.xpath('.//div[@class="span8 "]/span[@class="sfx-text "]/b/text()').extract_first()
            if name:

                agent_data['first_name'], agent_data['last_name'] = name.strip().split(maxsplit=1)
            else:
                agent_data['first_name'] = ''
                agent_data['last_name'] = ''

            company = agent.xpath('.//div[@class="span8 "]/div[@class="row-fluid tenPixel-topSpace"]/b/text()').extract_first()
            if company:
                agent_data['company'] = company.strip()
            else:
                agent_data['company'] = ''

            hidden_phone = agent.xpath('.//div[@class="span8 "]/div[@class="hidden-phone"]/div/span/text()')
            if len(hidden_phone) == 3:
                address_1 = hidden_phone[0].extract()
                address_2 = hidden_phone[1].extract()
                agent_data['address'] = address_1.strip() + ' ' + address_2.strip()

                puzzle = hidden_phone[2].extract()
                city, state_code = puzzle.split(', ')
            else:
                address_1 = hidden_phone[0].extract()
                agent_data['address'] = address_1.strip()

                puzzle = hidden_phone[1].extract()
                city, state_code = puzzle.split(', ')


            agent_data['city'] = city.strip()

            state_abbr, code = state_code.split()
            agent_data['state'] = state_abbr.strip()
            agent_data['code'] = code.strip()

            phone = agent.xpath('.//div[@class="span8 "]/div[@class="visible-phone"]/following-sibling::div/div[@class="row-fluid "]/div[@class="hidden-phone"]/span/text()').extract_first()
            if phone:
                agent_data['phone'] = phone.strip()
            else:
                agent_data['phone'] = ''

            lic = agent.xpath('.//div[@class="span8 "]/div[@class="visible-phone"]/following-sibling::div/div[@class="row-fluid "]/span/text()').extract_first()
            if lic:
                agent_data['license'] = lic.replace('Lic: ', '')
            else:
                agent_data['license'] = ''


            yield agent_data

    def close(self, reason):
        csv_file = 'statefarm_agents.csv'

        wb = Workbook()
        ws = wb.active

        with open(csv_file) as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save('statefarm_agents.xlsx')
