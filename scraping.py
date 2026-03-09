
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers={
    'User-Agent':'Mozilla/5.0'
}

#collectr data
crypto_data = []
coin_count = 0

#loop through pages
for page in range(1,50):
    print(f"Scraping page {page}..")

    url = f'https://coinmarketcap.com/?page={page}'
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")
    rows = soup.find_all('tr')
    records_on_page = 0

    for row in rows:
        tds = row.find_all('td')
        if len(tds) > 9:
            data = {}

            #coin name 
            name_tag = tds[2].find('p',class_='coin-item-name')
            data['Coin Name'] = name_tag.text.strip() if name_tag else 'N/A'

            #coin name 
            symbol_tag = tds[2].find('p',class_='coin-item-symbol')
            data['Symbol'] = symbol_tag.text.strip() if symbol_tag else 'N/A'

            #price 
            price_tag = tds[3].find('span')
            data['Price (USD)'] = price_tag.text.strip() if price_tag else 'N/A'

            #1h change
            change_1h = tds[4].find('span')
            data['1h change(%)'] = change_1h.text.strip() if change_1h else 'N/A'

            #24h change
            change_24h = tds[5].find('span')
            data['24h change(%)'] = change_24h.text.strip() if change_24h else 'N/A'

            #7d change
            change_7d = tds[6].find('span')
            data['7d change(%)'] = change_7d.text.strip() if change_7d else 'N/A'

            #Market cap
            market_cap = tds[7].find_all('span')
            data['Market Cap'] = market_cap[-1].text.strip() if market_cap else 'N/A'

            #volume(24h)
            volume_container = tds[8]
            volume_usd_tag = volume_container.find('a')
            if volume_usd_tag:
                volume_usd_p = volume_usd_tag.find('p')
                data['volume (24h) USD'] = volume_usd_p.text.strip() if volume_usd_p else 'N/A'
            

            #Circulating Supply
            supply_tag = tds[9].find('span')
            data['Circulating Supply'] = supply_tag.text.strip() if supply_tag else 'N/A'

            crypto_data.append(data)
            records_on_page += 1
            coin_count += 1

            if coin_count == 200:
                break

    print(f"Records scraped on page {page}: {records_on_page}")

    if coin_count == 200:
        break

    time.sleep(2)

#convert to dataframe
df = pd.DataFrame(crypto_data)

#save to excel
df.to_excel("Crypto_Analysiss_dataa.xlsx",index=False)
print("DONE: Exactly 200 coins scraped and saved successfully")



