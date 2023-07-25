import requests
import keys
import pandas as pd
from time import sleep

#call API and retrieve the price of BTC, ETH, and XRP
def get_crypto_rates(base_currency='USD', assets='BTC,ETH,XRP'):
    url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD,EUR'

    # Holds all parameters to insert into API endpoint, provides convert value and ID
    payload = {'key': keys.CRYPTOCOMPARE_API_KEY, 'convert': base_currency, 'ids': assets, 'interval': '1d'}
    response = requests.get(url, params=payload)
    data = response.json()


    # Initalize lists to hold asset name and price
    crypto_currency, crypto_price, crypto_timestamp = [], [], []

    # Loops through data and appends asset name to the crypto currency list, and appends price value to crypto price list
    for asset, currency_data in data.items():
        crypto_currency.append(asset)
        crypto_price.append(currency_data['USD'])
  
    raw_data = {
        'assets': crypto_currency,
        'rates': crypto_price,
    }

    # Creates Dataframe and inserts raw data
    df = pd.DataFrame(raw_data)
    return df


def set_alert(dataframe, asset, alert_high_price):
    # Retrieves crypto value from data frame
    crypto_value = float(dataframe[dataframe['assets'] == asset]['rates'].item())

    # Creates string to hold asset name, crypto price, and target price
    details = f'{asset}: {crypto_value}, Target: {alert_high_price}'

    # If the crypto value is greater than or equal to the target price
    if crypto_value >= alert_high_price:
        print(details + ' << TARGET VALUE REACHED!')
    else: 
        print(details)

#Creates forever loop and prints the following every 30 seconds. Uses try-catch block to catch any exceptions
loop = 0
while True: 
    print(f'----------------({loop})---------------------)')

    try: 
        df = get_crypto_rates()
        set_alert(df, 'BTC', 2900.50)
        set_alert(df, 'ETH', 1950.39)
    except Exception as e: 
        print('Could not retrieve the data...Trying again.')

    loop += 1
    sleep(30)