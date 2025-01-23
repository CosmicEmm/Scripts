import pandas as pd
import lxml # not used directly, but pandas uses lxml internally for parsing
from sys import argv


scraper = pd.read_html(f'https://en.wikipedia.org/wiki/{argv[1]}')
print(argv)

# for index, table in enumerate(scraper): # Iterates over the DataFrames
#     print('********************************************')
#     print(index)
#     print(table)

print(scraper[2]) # Prints the 3rd table (index 2) from the list of DataFrames