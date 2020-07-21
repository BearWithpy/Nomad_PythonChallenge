import os
import requests
from sys import stdin


def stripString(urls: list):
    urls_strip = []

    for url in urls:
        url = url.replace(" ", "").replace("\n", "").lower()
        urls_strip.append(url)

    return urls_strip


def checkURL(urls: list):
    for url in urls:
        if url[:7] != "http://":
            url = "http://" + url

        if url[-4:] != ".com":
            if url[-4:] != ".net":
                print(f"{url} is not a valid URL")
                continue

        try:
            res = requests.get(url)
            if res.status_code == 200:
                print(f"{url} is Up!")
            else:
                print(f"{url} is Down!")
        except:
            res = "No response"
            print(f"{url} is Down!")


while 1:
    os.system("clear")
    print("Welcome to IsItDown.py")
    print("Please write URLs you want to check. (Seperated by comma)")

    urls = list(map(str, stdin.readline().split(",")))

    urls = stripString(urls)
    checkURL(urls)

    ans = input("Do you want to start over? y/n ")
    while 1:
        if ans == "y" or ans == "Y":
            break
        elif ans == "n" or ans == "N":
            break
        else:
            print("That's not a valid answer")
            ans = input("Do you want to start over? y/n ")
    if ans == "y" or ans == "Y":
        continue
    elif ans == "n" or ans == "N":
        break

print("\nOk, bye")
a = 1
b = 2
