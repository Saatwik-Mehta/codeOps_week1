""" Copyright information """
__author__ = "Saatwik-Mehta"
__copyright__ = "Copyright (C) 2021 Saatwik-Mehta"
__license__ = "Public Domain"
__version__ = "1.0"


import logging
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
logging.basicConfig(filename="PriceTreeLoggings.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%("
                                                                                  "message)s")

with open("PriceComp.json", "r") as f:
    data = json.load(f)


for i in data['data']:
    """ Casting price data from String to float
     value in i['Best_Price'] = '78,900.00'"""

    price = float(re.sub(r'[^\d.]', '', i['Best_Price']))
    '''
    re.sub will substitute only the values other than a digit(0-9) and period(.)
    with ''.price variable will contain the float value only.
    For eg:
    price = 78900.00
    '''

    i['Best_Price'] = float(price)

df = pd.DataFrame(data['data'], columns=['Seller_Name', 'Best_Price'])

logging.debug(df)

seller_ls = []
# Seller_ls will contain Seller name unique values
price_ls = []
# price_ls will contain price that each company offers in the respective order

seller_ls.extend(df.Seller_Name.unique())
for comp in seller_ls:
    price_ls.append(min([df['Best_Price'][i] for i in df['Seller_Name'].index[df['Seller_Name'] == comp]]))

low_prices_df = pd.DataFrame(data={'Seller_Name': seller_ls, 'Best_Price': price_ls})
low_prices_sorted_df = low_prices_df.sort_values('Best_Price', ascending=True)

plt.style.use('bmh')

# Bar-Graph
plt.title("Samsung Galaxy Note 4 Price")
plt.bar(low_prices_sorted_df['Seller_Name'], low_prices_sorted_df['Best_Price'])
plt.ylabel("Best_Price")
plt.xlabel("Seller_Name")
plt.legend(["Price Tag"])
plt.show()

# Scatter Plot
plt.scatter(low_prices_sorted_df['Seller_Name'], low_prices_sorted_df['Best_Price'])
plt.title("Samsung Galaxy Note 4 Price")
plt.ylabel("Best_Price")
plt.xlabel("Seller_Name")
plt.legend(["Price Tag"])
plt.show()

# PieChart
plt.title("Samsung Galaxy Note 4 Price Comparison", loc="left", fontdict={'size': 11}, rotation=13)
plt.pie(low_prices_sorted_df['Best_Price'], labels=low_prices_sorted_df['Seller_Name'],
        autopct='% 1.1f %%', shadow=True, explode=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2], radius=1.2)
plt.legend(loc="center", title="Price share", fontsize=9)
plt.show()
