import csv
import json
from pathlib import Path

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
    sunshines.sort(reverse=True)  # fall back to latest data first
    employees = {}  # (fstname, lstname) -> [positions], [totalcomps]

    for f in sunshines:
        reader = csv.reader(open(f, "r"))
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue

            # parse data
            fstname = row[0].strip().upper()
            lstname = row[1].strip().upper()
            if not fstname or not lstname:
                continue

            role = row[2].strip()

            salary = float(row[3].strip().replace(" ", "").replace("$", "").replace(",", ""))
            benefits = float(row[4].strip().replace(" ", "").replace("$", "").replace(",", ""))
            totalcomp = float(salary + benefits)

            # insert if not exists
            if (fstname, lstname) not in employees:
                employees[(fstname, lstname)] = [[], []]
            employees[(fstname, lstname)][0].append(role)
            employees[(fstname, lstname)][1].append(totalcomp)

    employees = [{"firstname": k[0], "lastname": k[1], "positions": v[0], "totalcomps": v[1]} for k, v in employees.items()]
    with open(outputpath / "sunshines.json", "w") as f:
        json.dump(employees, f, indent=4)


merge_sunshines()
