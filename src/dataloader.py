import csv
import json
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

outputpath = Path("__file__").parent / "data"


"""
scraping data
"""


def download_csrankings():
    url = "https://raw.githubusercontent.com/emeryberger/CSrankings/refs/heads/gh-pages/csrankings.csv"
    if (outputpath / "csrankings.csv").exists():
        print("file already exists")
        return
    page = requests.get(url)
    assert page.status_code == 200

    page = requests.get(url)
    assert page.status_code == 200
    with open(outputpath / "csrankings.csv", "wb") as f:
        f.write(page.content)


def download_uwaterloos_sunshines_old(year):
    prefix = "https://uwaterloo.ca/about/accountability/salary-disclosure-"
    url = f"{prefix}{year}"
    if (outputpath / f"sunshines_{year}.csv").exists():
        print("file already exists")
        return

    page = requests.get(url)
    assert page.status_code == 200
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")
    schema = [th.text.replace(",", " ") for th in table.find("thead").find_all("th")]
    tbody = table.find("tbody")

    with open(outputpath / f"sunshines_{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(schema)
        for tr in tbody.find_all("tr"):
            writer.writerow([td.text.replace(",", " ") for td in tr.find_all("td")])


def download_uwaterloos_sunshines_new(year):
    prefix = "https://uwaterloo.ca/about/accountability/salary-disclosure-"
    url = f"{prefix}{year}"
    if (outputpath / f"sunshines_{year}.csv").exists():
        print("file already exists")
        return

    page = requests.get(url)
    assert page.status_code == 200
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")
    tbody = table.find("tbody")
    for td in tbody.find_all("td"):
        td.string = td.text  # drop useless <span>
    schema = [th.text.replace(",", " ") for th in table.find_all("th")]  # find schema in body

    with open(outputpath / f"sunshines_{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(schema)
        for tr in tbody.find_all("tr"):
            row = [td.text.replace(",", " ") for td in tr.find_all("td")]
            if any(row):
                writer.writerow(row)


download_csrankings()
download_uwaterloos_sunshines_old(2020)
download_uwaterloos_sunshines_old(2021)
download_uwaterloos_sunshines_old(2022)
download_uwaterloos_sunshines_new(2023)


"""
preprocessing data
"""


def merge_sunshines():
    if (outputpath / "sunshines.json").exists():
        print("file already exists")
        return

    sunshines = list(outputpath.glob("sunshines_*.csv"))
    employees = {}  # key: (firstname, lastname)

    """
    {
        "firstname": str,
        "lastname": str,
        "years": [
            {
                "year": int,
                "role": str,
                "salary": float,
                "benefits": float
            }
        ]
    }
    """

    for f in sunshines:
        year = int(f.stem.split("_")[1])

        reader = csv.reader(open(f, "r"))
        next(reader)

        for row in reader:
            row = [elem.strip() for elem in row]
            row = [re.sub(r"\s+", " ", elem) for elem in row]

            if (len(row) == 0) or any([len(elem) == 0 for elem in row]):
                continue

            fstname = row[0]
            lstname = row[1]
            role = row[2]
            salary = float(row[3].replace(" ", "").replace("$", "").replace(",", ""))
            benefits = float(row[4].replace(" ", "").replace("$", "").replace(",", ""))

            if (fstname, lstname) not in employees:
                employees[(fstname, lstname)] = {
                    "firstname": fstname,
                    "lastname": lstname,
                    "years": []
                }
            employees[(fstname, lstname)]["years"].append({
                "year": year,
                "role": role,
                "salary": salary,
                "benefits": benefits
            })

    with open(outputpath / "sunshines.jsonl", "w") as f:
        for employee in employees.values():
            f.write(json.dumps(employee) + "\n")

merge_sunshines()
