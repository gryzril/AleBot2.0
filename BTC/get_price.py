# https://linuxhit.com/how-to-easily-get-bitcoin-price-quotes-in-python/
import requests
  
  
# method to get the price of bit coin
def get_price():

    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data["bpi"]["USD"]["rate"]
  
