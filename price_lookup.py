from bs4 import BeautifulSoup 
import requests
import pandas as pd
from datetime import date

def url_to_price(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    price_table = soup.find_all('dt', class_= 'col-6 col-xl-5')

    columns = []
    for row in price_table:
        columns.append(row.text)

    if "Reprints" in columns:
        result = soup.find_all('dd', class_ = 'col-6 col-xl-7')[5].text.strip("€ ") # 5 is the trend-price
    else:
        result = soup.find_all('dd', class_ = 'col-6 col-xl-7')[4].text.strip("€ ") # 4 is the trend-price
    
    result = result.replace(",", ".") # change non-USA format of numbers to USA     
    result = result.replace(".", "", result.count(".") -1) # change non-USA format of numbers to USA     
    return float(result)

def update_reserved_list():
    data = pd.read_excel("reserved_list.xlsx")

    current_date = str(date.today())
    current_date = str(current_date).replace("-","_")

    data[f"price_{current_date}"] = data["mcm_link"].apply(lambda x: url_to_price(x))
    data["price"] = data[f"price_{current_date}"]

    data.to_excel("reserved_list.xlsx")

def update_non_reserved_list():
    data = pd.read_excel("non_reserved_list.xlsx")

    current_date = str(date.today())
    current_date = str(current_date).replace("-","_")

    data[f"price_{current_date}"] = data["mcm_link"].apply(lambda x: url_to_price(x))
    data["price"] = data[f"price_{current_date}"]

    data.to_excel("non_reserved_list.xlsx")

if __name__ == "__main__":
    update_reserved_list()
    update_non_reserved_list()
    