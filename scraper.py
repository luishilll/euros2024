import requests
import pandas as pd
from bs4 import BeautifulSoup


urls = ["https://fbref.com/en/comps/676/2021/schedule/2021-European-Championship-Scores-and-Fixtures"
    , "https://fbref.com/en/comps/676/2016/schedule/2016-European-Championship-Scores-and-Fixtures",
        "https://fbref.com/en/comps/676/2012/schedule/2012-European-Championship-Scores-and-Fixtures",
        "https://fbref.com/en/comps/676/2008/schedule/2008-European-Championship-Scores-and-Fixtures",
        "https://fbref.com/en/comps/676/2004/schedule/2004-European-Championship-Scores-and-Fixtures"]


def get_data(url):
    response = requests.get(url)
    html = response.content  # get website content

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")  # get table and rows

    headers = [header.text for header in rows[0].find_all("th") if header.text != "xG"]


    data = []
    for row in rows[1:]:
        cells = row.find_all('td')
        if not all(item == "" for item in [cell.text for cell in cells]):
            data.append([cell.text for cell in cells])  # get data from each row td, starting from second row to not include headers

    if url == "https://fbref.com/en/comps/676/2021/schedule/2021-European-Championship-Scores-and-Fixtures" or url == "https://fbref.com/en/comps/676/schedule/European-Championship-Scores-and-Fixtures":
        for row in data:
            row.pop(5)
            row.pop(6)
        df = pd.DataFrame(data, columns=headers[1:]) # 2021 euros has xG column, so get rid of that so it matches others
    else:
        df = pd.DataFrame(data, columns=headers[1:])
    return df


dataframes = [get_data(url) for url in urls]


main_table = pd.concat(dataframes, ignore_index=True)

pred_url = "https://fbref.com/en/comps/676/schedule/European-Championship-Scores-and-Fixtures"

pred = get_data(pred_url)

pred.to_csv(r"C:\Users\luish\PycharmProjects\euros2024\euros2024\test_data.csv", index=False)


main_table.to_csv(r"C:\Users\luish\PycharmProjects\euros2024\euros2024\data.csv", index=False)
