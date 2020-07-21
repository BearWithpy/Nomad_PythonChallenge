import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"


def rere(country):

    try:
        number = int(input("#: "))
        if number >= len(country):
            print("Choose a number from the list.")
            rere(country)

        elif number < 0:
            print("Choose a number from the list.")
            rere(country)

        else:
            print(f"You chose {country[number]['country']}")
            print(f"The currency code {country[number]['code']}")
            return

    except:
        print("That wasn't a number")
        rere(country)


def main():
    print("Hello! Please chose select a country by number")

    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find("table").find_all("tbody")[0].find_all("tr")

    country = []
    for t in table:
        info = dict()
        info["country"] = t.find_next("td").string.lower().title()
        info["currency"] = t.find_next("td").find_next("td").string
        info["code"] = info["currency"].find_next("td").string
        if info["code"] is None:
            continue
        info["number"] = info["code"].find_next("td").string
        country.append(info)

    for idx, cn in enumerate(country):
        print(f"#{idx} {cn['country']}")

    rere(country)


main()
