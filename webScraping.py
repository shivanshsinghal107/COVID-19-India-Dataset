import requests
import subprocess
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_table():
    url = 'https://www.mohfw.gov.in/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    table_no = len(soup.findAll("table"))
    table = soup.findAll("table")[table_no - 1]
    return table

def get_headers(table):
    # scarping headers
    headers = []
    for th in table.find('tr').findAll('th'):
        headers.append(th.text.strip())
    return headers

def get_rows(table):
    rows = []
    for tr in table.findAll('tr')[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.findAll('td')
        if(len(tds) == 0):
            # if no td tags search th tags
            ths = tr.findAll('th')
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows

def get_dataframe():
    # making csv of the data
    table = get_table()
    headers = get_headers(table)
    rows = get_rows(table)
    table_name = "covid_india"
    #converting csv to dataframe
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")
    df = pd.read_csv(f"{table_name}.csv")
    return df

def get_inddata():
    df = get_dataframe()
    df.dropna(inplace = True)
    df.drop(columns = ['Unnamed: 0', 'S. No.'], inplace = True)
    df.columns = ['State/UT', 'Confirmed', 'Recovered', 'Deaths']
    df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']
    df = df[['State/UT', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    df = df.sort_values(by = 'Confirmed', ascending = False).reset_index(drop = True)
    return df
