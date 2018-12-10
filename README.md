# Scrapy spiders for 5 different sites

## 1st spider
## Scraping all American banks.  

#### Algorithm
1. Go through each state
2. Go through all available cities
3. Go inside detail page of each bank
4. Scrape 27 fields: Name,	Branch,	Address,	City,	State,	ZIP,	County,	Phone,	Branch Deposit,	Type,	Website	URL,	Concentration,	Established,	Holden By,	Charter Class,	# of branches,	Total Assets,	Total Deposits,	Total Equity Capital,	Total Domestic Office Deposits,	Net Income,	Quartly Net Income,	ROA,	QROA,	ROE,	QROE

5. Save results in .xlsx file

![usbanklocations](https://i.imgur.com/QUGenTV.png)

## 2nd spider
## Scraping all countryfinancial agents for all US zip codes

#### Algorithm
1. Request through all ZIP codes
2. Get all agents profiles links
3. Go inside each profile detail page
4. Scrape 12 fields: First Name, Last Name,	Address,	City,	State,	ZIP,	Office Phone,	Cell Phone,	Email,	LinkedIn,	Facebook,	Site URL
5. Save results in .xlsx file

![countryfinancial](https://i.imgur.com/5tgHs4i.png)

## 3rd spider
## Scraping 1707 agents profiles from Farm Bureau Financial Services  

#### Algorithm
1. Go through each profile URL
2. Scrape 10 fields: Street,	Locality,	Region,	Postal code,	Name,	Designations,	Itemscope,	Phone,	Fax,	Email
5. Save results in .csv file

![bureau](https://i.imgur.com/uqqVw9R.png)

## 4th spider
## Scraping all StateFarm agents profiles  

#### Algorithm
1. Go through each state
2. Go through all available cities
3. Go inside each profile detail page
4. Scrape 8 fields: First Name,	Last Name, Address,	City,	State, Code,	Phone, License
5. Save results in .xlsx file

![statefarm](https://i.imgur.com/iaNpgp1.png)

## 5th spider
## Scraping all construction equipment  

#### Algorithm
1. Go only through manufacturers that have many models of equipment
2. Get all available models for each manufacturer
3. Scrape 2 fields: Make, Model
4. Save results in .csv file

![machinerytrader](https://i.imgur.com/hCNSo1r.jpg)  

![machinerytrader_models](https://i.imgur.com/sSfATLq.png)
