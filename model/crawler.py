import yfinance as yf
import requests
import bs4 as bs


# crawl list of tickers from wikipedia
html = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})

tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    ticker = ticker[:-1]
    tickers.append(ticker)


# save data from yahoo finance to csv
for ticker in tickers:
    data = yf.download(ticker, start="2009-01-01", end="2021-12-31", interval="3mo")
    data.to_csv(f'data/ticker_{ticker}.csv')