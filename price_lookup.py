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

def update_price_list(excel_file):
    data = pd.read_excel(excel_file)

    current_date = str(date.today()).replace("-","_")
    
    data[f"price_{current_date}"] = data["mcm_link"].apply(lambda x: url_to_price(x))
    data["price"] = data[f"price_{current_date}"]

    data.to_excel(excel_file)

if __name__ == "__main__":
    update_price_list("reserved_list.xlsx")
    update_price_list("non_reserved_list.xlsx")
    