import csv
import json
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from tqdm import tqdm

outputpath = Path("__file__").parent / "data"


"""
uwaterloo salary disclosures, merging years 2020-2023
"""


def get_sunshines_old(year):
    prefix = "https://uwaterloo.ca/about/accountability/salary-disclosure-"
    url = f"{prefix}{year}"
    if (outputpath / f"sunshines{year}.csv").exists():
        print("file already exists")
        return

    page = requests.get(url)
    assert page.status_code == 200
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")
    schema = [th.text.replace(",", " ") for th in table.find("thead").find_all("th")]
    tbody = table.find("tbody")

    with open(outputpath / f"sunshines{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(schema)
        for tr in tbody.find_all("tr"):
            writer.writerow([td.text.replace(",", " ") for td in tr.find_all("td")])


def get_sunshines_new(year):
    prefix = "https://uwaterloo.ca/about/accountability/salary-disclosure-"
    url = f"{prefix}{year}"
    if (outputpath / f"sunshines{year}.csv").exists():
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

    with open(outputpath / f"sunshines{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(schema)
        for tr in tbody.find_all("tr"):
            row = [td.text.replace(",", " ") for td in tr.find_all("td")]
            if any(row):
                writer.writerow(row)


def merge_sunshines():
    if (outputpath / "sunshines-v1.json").exists():
        print("file already exists")
        return

    sunshines = list(outputpath.glob("sunshines*.csv"))
    employees = {}  # key: (firstname, lastname)

    for f in sunshines:
        year = int(f.stem[-4:])

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
                employees[(fstname, lstname)] = {"firstname": fstname, "lastname": lstname, "years": []}
            employees[(fstname, lstname)]["years"].append({"year": year, "role": role, "salary": salary, "benefits": benefits})

    with open(outputpath / "sunshines-v1.jsonl", "w") as f:
        for employee in employees.values():
            f.write(json.dumps(employee) + "\n")


get_sunshines_old(2020)
get_sunshines_old(2021)
get_sunshines_old(2022)
get_sunshines_new(2023)
merge_sunshines()


"""
joining sunshines with csrankings to find scholarids (not effective)
"""


def get_csrankings():
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


def join_csrankings():
    if (outputpath / "sunshines-v2.jsonl").exists():
        print("file already exists")
        return

    sunshines = outputpath / "sunshines-v1.jsonl"
    csrankings = outputpath / "csrankings.csv"

    csrankings_df = pd.read_csv(csrankings)
    print(f"num all rows in csrankings: {len(csrankings_df)}")
    csrankings_df = csrankings_df[csrankings_df["affiliation"].str.contains("waterloo", case=False)]
    print(f"num uwaterloo rows csranking: {len(csrankings_df)}")
    print(f"num all rows in sunshines: {len(open(sunshines, 'r').readlines())}")

    def fuzzy_match(name1, name2, threshold=80):
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        ratio = fuzz.token_sort_ratio(name1, name2)
        return ratio >= threshold

    found_matches = 0
    with open(outputpath / "sunshines-v2.jsonl", "w") as f:
        for line in tqdm(open(sunshines, "r")):
            employee = json.loads(line)
            name = (employee["lastname"] + " " + employee["firstname"]).lower().strip()

            scholarids = set()
            for _, row in csrankings_df.iterrows():
                if fuzzy_match(name, row["name"]):
                    scholarids.add(row["scholarid"])
            if len(scholarids) > 0:
                found_matches += 1
            employee["scholarids_csr"] = list(scholarids)

            f.write(json.dumps(employee) + "\n")

    print(f"found matches: {found_matches}")


get_csrankings()
join_csrankings()



"""
joining sunshines with semantic scholar to find scholarids (effective)
"""

# https://api.semanticscholar.org/graph/v1/author/search?query=

def join_sscholar():
    print("yo")

join_sscholar()
