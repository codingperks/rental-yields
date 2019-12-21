#!usr/bin/env python

'''
    Author =  Ryan Perkins
    Date of Creation: 20/12/19
    Date of last edit: 20/12/19
    Description: This script scrapes the rental yields for european countries from globalpropertyguide.com.
        This script then filters for countries of interest and then exports these to an excel file
'''


# Module dependencies
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Creating dict to store data in
rental_yields = {}

# Setting up URL
url = 'https://www.globalpropertyguide.com/Europe'

# Setting data to URL
data = requests.get(url)
page_content = data.content

# Parse html into soup
soup = BeautifulSoup(page_content, features='html.parser')

# Using soup to obtain table and isolate the rows
table = soup.findAll("table")[0].findAll("tr")

# Loops over table rows
for row in table:
    # This line finds individual elements for each row in the table
    elements = row.find_all("td")

    # Strips empty space from elements
    elements = [element.text.strip() for element in elements]

    # Skips over empty rows
    if not elements:
        continue

    # Grabs country column
    country_name = elements[0]

    # Grabs rental yield column
    country_yield = elements[1]

    # Appends country and rental yield to dictionary made earlier
    rental_yields[country_name] = country_yield

# Some countries have 'Not Rated' as their value. This replaces these values with missing (NaN)
for key, value in rental_yields.items():
    if value == "Not Rated":
        rental_yields[key] = np.nan

# Converts string rental yield values to float (for creation of data frame)
for k, v in rental_yields.items():
    rental_yields[k] = float(v)

# Converts dictionary into data frame with two columns for Country and Yield, using dict keys and values
df = pd.DataFrame(list(rental_yields.items()), columns=['Country', 'Yield'])
print(df)

# We are only interested in subset of these countries, this list is used to remove non-used countries
country_list = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
                'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia',
                'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
                'Slovenia', 'Spain', 'United Kingdom']

# This command keeps countries of interest
df = (df[df["Country"].isin(country_list)])

# Exports to xls file
df.to_excel("rentalyields.xlsx", index=False)

# Authorship metadata
__author__ = "Ryan Perkins"
__copyright__ = "Copyright-free"
__credits__ = ["Ryan Perkins"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Ryan Perkins"
__email__ = "rperkins@londoneconomics.co.uk"
__status__ = "Production"