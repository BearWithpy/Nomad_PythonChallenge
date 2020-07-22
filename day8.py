import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")


def getLink(value):
    pages = []
    for i in value:
        name = i.find("span", {"class": "company"}).get_text(strip=True)
        link = i.find("a")["href"]

        brand_dict = {"company": name, "link": link}
        pages.append(brand_dict)

    return pages


def extract_jobs(pages):
    infos = []
    for i in range(len(pages)):
        print(f"Scrapping info {pages[i]['company']}...")
        url = pages[i]["link"]
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("tbody").find_all("tr")

        for tr in table:
            t = tr.find_all("td")
            if len(t) == 5:
                info = dict()
                info["place"] = t[0].get_text().replace("\xa0", " ")
                title = t[1].find("span", {"class": "company"})
                if title is not None:
                    title = title.get_text(strip=True)
                info["title"] = title
                info["time"] = t[2].get_text()
                info["pay"] = t[3].get_text()
                info["date"] = t[4].get_text()
                # print(info)
                infos.append(info)
            else:
                pass

    return infos


def save_to_jobs(brand, jobs):
    # print(jobs)
    # return
    for i in range(len(brand)):
        with open(f"{brand[i]['company']}.csv", mode="w", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["place", "title", "time", "pay", "date"])
            for job in jobs:
                writer.writerow(list(job.values()))


def main():

    alba_url = "http://www.alba.co.kr"

    result = requests.get(alba_url)
    soup = BeautifulSoup(result.text, "html.parser")
    value = (
        soup.find(id="MainSuperBrand").find("ul", {"class": "goodsBox"}).find_all("li")
    )

    brand = getLink(value)
    # print(brand)
    jobs = extract_jobs(brand)
    save_to_jobs(brand, jobs)


main()


# nico code
#
# import os
# import csv
# import requests
# from bs4 import BeautifulSoup
#
# os.system("clear")
#
#
# def write_company(company):
#     file = open(f"{company['name']}.csv", mode="w")
#     writer = csv.writer(file)
#     writer.writerow(["place", "title", "time", "pay", "date"])
#     for job in company["jobs"]:
#         writer.writerow(list(job.values()))
#
#
# alba_url = "http://www.alba.co.kr"
#
# alba_request = requests.get(alba_url)
# alba_soup = BeautifulSoup(alba_request.text, "html.parser")
# main = alba_soup.find("div", {"id": "MainSuperBrand"})
# brands = main.find_all("li", {"class": "impact"})
# for brand in brands:
#     link = brand.find("a", {"class": "goodsBox-info"})
#     name = brand.find("span", {"class": "company"})
#     if link and name:
#         link = link["href"]
#         name = name.text
#         company = {"name": name, "jobs": []}
#         jobs_request = requests.get(link)
#         jobs_soup = BeautifulSoup(jobs_request.text, "html.parser")
#         tbody = jobs_soup.find("div", {"id": "NormalInfo"}).find("tbody")
#         rows = tbody.find_all("tr", {"class": ""})
#         for row in rows:
#             local = row.find("td", {"class": "local"})
#             if local:
#                 local = local.text.replace("\xa0", " ")
#             title = row.find("td", {"class": "title"})
#             if title:
#                 title = title.find("a").find("span", {"class": "company"}).text.strip()
#                 title = title.replace("\xa0", " ")
#             time = row.find("td", {"class": "data"})
#             if time:
#                 time = time.text.replace("\xa0", " ")
#             pay = row.find("td", {"class": "pay"})
#             if pay:
#                 pay = pay.text.replace("\xa0", " ")
#             date = row.find("td", {"class": "regDate"})
#             if date:
#                 date = date.text.replace("\xa0", " ")
#             job = {
#                 "place": local,
#                 "title": title,
#                 "time": time,
#                 "pay": pay,
#                 "date": date,
#             }
#             company["jobs"].append(job)
#         write_company(company)
