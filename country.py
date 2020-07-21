import os
import requests
from bs4 import BeautifulSoup

os.system("clear")


def rere(country):
    first_country = ""
    second_country = ""
    while 1:
        try:
            print("\nWhere are you from? Choose a country BY NUMBER.\n")
            number = int(input("#: "))
            if number >= len(country):
                print("Choose a number from the list.")
                continue

            elif number < 0:
                print("Choose a number from the list.")
                continue

            else:
                print(f"{country[number]['country']}\n")
                first_country = country[number]["code"]
                while 1:
                    try:
                        print("Now choose another country.\n")
                        number = int(input("#: "))
                        if number >= len(country):
                            print("Choose a number from the list.")
                            continue

                        elif number < 0:
                            print("Choose a number from the list.")
                            continue

                        else:
                            print(f"{country[number]['country']}\n")
                            second_country = country[number]["code"]
                            break
                    except:
                        print("That wasn't a number")
                        continue

                return [first_country, second_country]

        except:
            print("That wasn't a number")
            continue


def iban():

    url = "https://www.iban.com/currency-codes"

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

    return rere(country)
