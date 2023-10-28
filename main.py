# import required modules
from bs4 import BeautifulSoup
import pandas as pd
import requests

pd.set_option('display.max_rows', None)

# get URL
page = requests.get("https://en.wikipedia.org/wiki/List_of_animal_names")

# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')

list(soup.children)

columns = ['Animal','Yound','Female','Male','Collective noun','Collateral adjective','Culinary noun for meat']

table = soup.find_all('table')[2]

table_rows = table.find_all('tr')

def custom_operation_CollNoun(c):
    cc = c.text.split(']')
    if cc[-1] == '':
        cc.pop()
    cc = [s for s in cc if not (s.isdigit() or s.startswith('[') or not s)]
    for i in range(len(cc)):
        last_char = cc[i][-1]
        while last_char.isdigit() or last_char == '[':
            cc[i] = cc[i][:-1]
            last_char = cc[i][-1]
    return cc

l = []
for tr in table_rows:
    td = tr.find_all('td')
    modified_row = [custom_operation_CollNoun(c) if i==4 else c.get_text(strip=True) for i, c in enumerate(td)]
    l.append(modified_row)
df = pd.DataFrame(l, columns=columns)

# New DataFrame
new_columns = ['Animal', 'Coll']
new_df = pd.DataFrame(columns=new_columns)

# Function to apply logic and populate new_df
def process_row(row):
    if row['Collective noun'] == ['—'] or row['Collective noun'] == None or row['Collective noun'] == ['?']:
        new_row = {'Animal': row['Animal'], 'Coll': row['Collateral adjective']}
        new_df.loc[len(new_df)] = new_row
    elif isinstance(row['Collective noun'], list):
        for value in row['Collective noun']:
            new_row = {'Animal': row['Animal'], 'Coll': value}
            new_df.loc[len(new_df)] = new_row

# Apply the function to each row of the original DataFrame
df.apply(process_row, axis=1)

new_df.dropna(how='all', inplace=True)

# Resetting the index of the new DataFrame
new_df.reset_index(drop=True, inplace=True)

print(new_df.to_string())