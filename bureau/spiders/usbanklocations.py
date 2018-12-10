# -*- coding: utf-8 -*-
import csv
import scrapy
import re

from openpyxl import Workbook


class UsbanklocationsSpider(scrapy.Spider):
    name = 'usbanklocations'
    allowed_domains = ['usbanklocations.com']
    start_urls = ['https://www.usbanklocations.com/']

    def parse(self, response):
        us_states = response.xpath('(//td[a[contains(text(), "Alabama")]]/a/@href | //td[a[contains(text(), "Montana")]]/a/@href)').extract()
        for state in us_states[:1]:
            yield response.follow(state.replace('s.htm', '-list.htm'), callback=self.parse_state_banks)
    
    def parse_state_banks(self, response):
        state_banks = response.xpath('//div[@class="resultsListBig"]/a/@href')
        for bank in state_banks:
            yield response.follow(bank, callback=self.parse_branches)
    
    def parse_branches(self, response):
        branches = response.xpath('(//div[@class="plb"] | //div[@class="plw"])/b/a/@href')
        for branch in branches:
            yield response.follow(branch, callback=self.parse_target)
        
        next_page = response.xpath('//div[@class="plb"]/preceding-sibling::div[@class="panelpn"]/a[contains(text(),"next")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_branches)
    
    def parse_target(self, response):
        bank_data = {}

        # Parse 1st table
        header = response.xpath('//h1/text()').extract_first()
        if header:
            if ',' in header:
                bank, bank_branch = header.split(',', maxsplit=1)
                name = bank.strip()
                branch = bank_branch.strip()
            else:
                name = header
                branch = ''
        else:
            name = ''
            branch = ''
        
        bank_data['Name'] = name
        bank_data['Branch'] = branch

        table_organization = response.xpath('//h1/following-sibling::table[contains(@typeof, "Organization")]//table')
        
        bank_data['Address'] = table_organization.xpath('.//span[@property="v:street-address"]/text()').extract_first()
        bank_data['City'] = table_organization.xpath('.//span[@property="v:locality"]/text()').extract_first()
        bank_data['State'] = table_organization.xpath('.//span[@property="v:region"]/text()').extract_first()
        bank_data['ZIP'] = table_organization.xpath('.//span[@property="v:postal-code"]/text()').extract_first()

        county = table_organization.xpath('.//span[@rel="v:address"]/following-sibling::text()').extract_first()
        if county:
            county = county.replace('County', '').strip()
        bank_data['County'] = county

        bank_data['Phone'] = table_organization.xpath('.//td[@property="v:tel"]/text()').extract_first()
        bank_data['Branch Deposit'] = table_organization.xpath('.//td[contains(string(), "Branch Deposit")]/following-sibling::td/text()').extract_first()
        bank_data['Type'] = table_organization.xpath('.//span[@property="v:name"]/following-sibling::text()[last()]').extract_first()

        # Parse 2nd table
        table_bank = response.xpath('//h1/following-sibling::table[contains(@typeof, "Organization")]/following-sibling::table')
        
        bank_data['Website'] = table_bank.xpath('.//td[contains(string(), "Website")]/following-sibling::td/a/text()').extract_first()
        bank_data['Link'] = table_bank.xpath('.//td[contains(string(), "Website")]/following-sibling::td/a/@href').extract_first()
        bank_data['Concentration'] = table_bank.xpath('.//td[contains(string(), "Concentration")]/following-sibling::td/text()').extract_first()
        bank_data['Established'] = table_bank.xpath('.//td[contains(string(), "Established")]/following-sibling::td/text()').extract_first()
        bank_data['Holden By'] = table_bank.xpath('.//td[contains(string(), "Holden By")]/following-sibling::td/text()').extract_first()
        bank_data['Charter Class'] = table_bank.xpath('.//td[contains(string(), "Charter Class")]/following-sibling::td/text()').extract_first()
        
        num_of_branches = table_bank.xpath('.//td[contains(string(), "# of Branches")]/following-sibling::td/text()').extract_first()
        if num_of_branches:
            num_of_branches = re.search(r'\d+', num_of_branches).group()
        
        bank_data['# of branches'] = num_of_branches
        bank_data['Total Assets'] = table_bank.xpath('.//td[contains(string(), "Total Assets")]/following-sibling::td/text()').extract_first()
        bank_data['Total Deposits'] = table_bank.xpath('.//td[contains(string(), "Total Deposits")]/following-sibling::td/text()').extract_first()
        bank_data['Total Equity Capital'] = table_bank.xpath('.//td[contains(string(), "Total Equity Capital")]/following-sibling::td/text()').extract_first()
        bank_data['Total Domestic Office Deposits'] = table_bank.xpath('.//td[contains(string(), "Total Domestic Office Deposits")]/following-sibling::td/text()').extract_first()
        bank_data['Net Income'] = table_bank.xpath('.//td[contains(string(), "Net Income")]/following-sibling::td/text()').extract_first()
        bank_data['Quartly Net Income'] = table_bank.xpath('.//td[contains(string(), "Quarterly Net Income")]/following-sibling::td/text()').extract_first()
        bank_data['ROA'] = table_bank.xpath('.//td[contains(string(), "Return on Assets")]/following-sibling::td/text()').extract_first()
        bank_data['QROA'] = table_bank.xpath('.//td[contains(string(), "Quarterly Return on Assets")]/following-sibling::td/text()').extract_first()
        bank_data['ROE'] = table_bank.xpath('.//td[contains(string(), "Return on Equity")]/following-sibling::td/text()').extract_first()
        bank_data['QROE'] = table_bank.xpath('.//td[contains(string(), "Quarterly Return on Equity")]/following-sibling::td/text()').extract_first()
        
        yield bank_data

    def close(self, reason):
        wb = Workbook()
        ws = wb.active

        with open('usbanklocations_alabama_to_check.csv') as f:
            for row in csv.reader(f):
                ws.append(row)
        
        wb.save('usbanklocations_alabama_to_check.xlsx')
