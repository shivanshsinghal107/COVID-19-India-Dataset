import requests
from bs4 import BeautifulSoup
import pandas as pd

res = requests.get("https://www.mygov.in/corona-data/covid19-statewise-status/")
soup = BeautifulSoup(res.text, "html.parser")
div = soup.select("#node-287111 > div > div.field-collection-container.clearfix > div > div.field-items")[0]

states_divs = div.find_all("div", {"class": "field field-name-field-select-state field-type-list-text field-label-above"})
states = []
for d in states_divs:
    name = d.find("div", {"class": "field-items"})
    states.append(name.text)

con_divs = div.find_all("div", {"class": "field field-name-field-total-confirmed-indians field-type-number-integer field-label-above"})
confirmed = []
for c in con_divs:
    cases = c.find("div", {"class": "field-items"})
    confirmed.append(int(cases.text))

cur_divs = div.find_all("div", {"class": "field field-name-field-cured field-type-number-integer field-label-above"})
cured = []
for c in cur_divs:
    cases = c.find("div", {"class": "field-items"})
    cured.append(int(cases.text))

death_divs = div.find_all("div", {"class": "field field-name-field-deaths field-type-number-integer field-label-above"})
deaths = []
for d in death_divs:
    cases = d.find("div", {"class": "field-items"})
    deaths.append(int(cases.text))

df = pd.DataFrame(states, columns = ['Name of State / UT'])
df['Total Confirmed cases'] = confirmed
df['Cured/Discharged/Migrated'] = cured
df['Deaths'] = deaths
df['Active Cases'] = df['Total Confirmed cases'] - df['Cured/Discharged/Migrated'] - df['Deaths']
df['S. No.'] = df.index + 1

df = df[['S. No.', 'Name of State / UT', 'Active Cases', 'Cured/Discharged/Migrated', 'Deaths', 'Total Confirmed cases']]

df.to_csv("covid_india.csv", index = False)
