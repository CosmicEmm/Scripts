import pandas as pd
import lxml # not used directly, but pandas uses lxml internally for parsing
from sys import argv


scraper = pd.read_html(f'https://en.wikipedia.org/wiki/{argv[1]}') #use _ instead of space in player name
print(argv)

# for index, table in enumerate(scraper): # Iterates over the DataFrames
#     print('********************************************')
#     print(index)
#     print(table)

index = int(argv[2])
print(scraper[index]) # Prints the table at the specified index from the list of DataFrames (e.g. index = 2 means 3rd table)