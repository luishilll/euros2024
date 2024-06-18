import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://fbref.com/en/comps/676/2021/schedule/2021-European-Championship-Scores-and-Fixtures"

response = requests.get(url)
html = response.content # get website content

soup = BeautifulSoup(html,"html.parser")

table = soup.find("table")
rows = table.find_all("tr")  # get table and rows

headers = [header.text for header in rows[0].find_all("th")]

data = []
for row in rows[1:]:
    cells = row.find_all('td')
    data.append([cell.text for cell in cells]) # get data from each row td, starting from second row to not include headers

print(headers)

df = pd.DataFrame(data, columns=headers[1:])

print(df["Home"])

df.to_csv("C:\Users\luish\PycharmProjects\euros2024\euros2024",index=False)



