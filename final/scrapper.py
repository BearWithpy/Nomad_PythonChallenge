import requests
from bs4 import BeautifulSoup
import re


def scrape_wework(term):
    url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception

    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("li", {"class": "feature"})

    result = []

    for job in jobs:
        a_tag = job.find_all("a")

        if len(a_tag) > 1:
            a_tag = a_tag[1]
        else:
            a_tag = a_tag[0]

        url = "https://weworkremotely.com" + a_tag["href"].strip()
        company = job.find("span", {"class": "company"}).get_text(strip=True)
        title = job.find("span", {"class": "title"}).get_text(strip=True)

        if all([url, title, company]):
            job_dict = {"url": url, "company": company, "title": title}
            result.append(job_dict)

    return result


def scrape_stackoverflow(term):
    url = f"https://stackoverflow.com/jobs?r=true&q={term}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception

    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    source = soup.find("div", attrs={"class": "listResults"})
    jobs = source.find_all("div", {"class": "grid"})

    result = []

    for job in jobs:
        s_link = job.find("a", {"class": "s-link"})
        if not s_link:
            continue
        url = "https://stackoverflow.com" + s_link["href"].strip()
        title = s_link["title"].strip()
        company = job.find("h3").find("span", {"class": ""}).get_text(strip=True)

        if all([url, title, company]):
            job_dict = {"url": url, "company": company, "title": title}
            result.append(job_dict)

    return result


def scrape_remoteok(term):
    url = f"https://remoteok.io/remote-dev+{term}-jobs"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception

    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    source = soup.find("table", {"id": "jobsboard"})
    jobs = source.find_all("td", {"class": "company_and_position"})

    result = []

    for job in jobs:
        # url = "https://remoteok.io" + job.find("a", {"class": "preventLink"})["href"]
        url = "https://remoteok.io" + job.find("a").get("href")

        # title = job.find("h2", {"itemprop": "title"}).get_text()
        title = job.find("h2", {"itemprop": "title"})
        title_text = re.sub("<.+?>", "", str(title), 0).strip()

        # company = job.find("h3", {"itemprop": "name"}).get_text()
        company = job.find("h3", {"itemprop": "name"})
        company_text = re.sub("<.+?>", "", str(company), 0).strip()

        if all([url, title, company]):
            job_dict = {"url": url, "company": company_text, "title": title_text}
            result.append(job_dict)

    return result
