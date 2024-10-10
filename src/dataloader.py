import csv
import json
import random
import re
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from tqdm import tqdm
from transformers import pipeline

outputpath = Path("__file__").parent / "data"


"""
get uwaterloo salary disclosures.
merge years 2020-2023.
"""


def get_sunshines_old(year):
    prefix = "https://uwaterloo.ca/about/accountability/salary-disclosure-"
    url = f"{prefix}{year}"
    if (outputpath / f"sunshines{year}.csv").exists():
        print("file already exists")
        return

    page = requests.get(url)
    assert page.status_code == 200, f"status code: {page.status_code}"
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
    assert page.status_code == 200, f"status code: {page.status_code}"
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
join salary disclosures with csrankings
"""


def fuzzy_match(name1, name2, threshold):
    assert 0 <= threshold <= 100
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    ratio = fuzz.token_sort_ratio(name1, name2)
    return ratio >= threshold


def get_csrankings():
    url = "https://raw.githubusercontent.com/emeryberger/CSrankings/refs/heads/gh-pages/csrankings.csv"
    if (outputpath / "csrankings.csv").exists():
        print("file already exists")
        return
    page = requests.get(url)
    assert page.status_code == 200, f"status code: {page.status_code}"

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

    found_matches = 0
    with open(outputpath / "sunshines-v2.jsonl", "w") as f:
        for line in tqdm(open(sunshines, "r")):
            employee = json.loads(line)
            name = (employee["lastname"] + " " + employee["firstname"]).lower().strip()

            scholarids = set()
            for _, row in csrankings_df.iterrows():
                if fuzzy_match(name, row["name"], threshold=80):
                    scholarids.add(row["scholarid"])
            if len(scholarids) > 0:
                found_matches += 1
            employee["csrankings_scholarids"] = list(scholarids)

            f.write(json.dumps(employee) + "\n")

    print(f"found matches: {found_matches}")


get_csrankings()
join_csrankings()


"""
join salary disclosures with semantic scholar
"""


def join_sscholar(retry=False):
    sunshines = outputpath / "sunshines-v2.jsonl"
    if not retry and sunshines.exists():
        print("file already exists")
        return
    outfile = outputpath / "sunshines-v3.jsonl"

    def is_cached(firstname, lastname):  # compute is cheaper than network
        content = open(outfile).read()
        for line in content.split("\n"):
            if len(line) == 0:
                continue
            employee = json.loads(line)
            if (employee["firstname"] == firstname) and (employee["lastname"] == lastname):
                return True
        return False

    def fetch_retry(url, max_retries=20):
        retries = 0
        while retries < max_retries:
            try:
                page = requests.get(url)
                page.raise_for_status()
                return page
            except:
                retries += 1
                time.sleep(random.uniform(1, 3))
        else:
            print(f"max retries reached...")
            exit(1)

    if not outfile.exists():
        open(outfile, "w").close()

    with open(outfile, "a") as out:
        for line in tqdm(open(sunshines, "r"), total=len(open(sunshines, "r").readlines())):
            employee = json.loads(line)
            if is_cached(employee["firstname"], employee["lastname"]):
                continue

            url = "https://api.semanticscholar.org/graph/v1/author/search?query="
            name_encoded = (employee["lastname"].replace(" ", "+") + "+" + employee["firstname"].replace(" ", "+")).lower().strip()
            suffix = "&fields=authorId,externalIds,name,paperCount,citationCount,hIndex"
            query = url + name_encoded + suffix
            page = fetch_retry(query)
            res = page.json()
            if (res["total"] <= 0) or (len(res["data"]) == 0):
                continue
            res = res["data"]

            # 1) fuzzy name match
            name = (employee["lastname"] + " " + employee["firstname"]).lower().strip()
            res = [elem for elem in res if fuzzy_match(name, elem["name"], threshold=80)]

            # 2) prefer options with externalIds
            if (len(res) > 1) and any([len(elem["externalIds"]) > 0 for elem in res]):
                res = [elem for elem in res if len(elem["externalIds"]) > 0]

            # 3) prefer highest performing author
            if len(res) > 1:
                res = sorted(res, key=lambda x: x["citationCount"] + x["paperCount"] + x["hIndex"], reverse=True)
                res = [res[0]]

            if len(res) == 0:
                continue
            res = res[0]
            out.write(json.dumps({**employee, **res}) + "\n")


join_sscholar(retry=False)


"""
preprocessing
"""


weightpath = Path("__file__").parent / "weights"
if not weightpath.exists():
    weightpath.mkdir()
gender_classifier = pipeline("text-classification", model="padmajabfrl/Gender-Classification", model_kwargs={"cache_dir": weightpath})


def get_final():
    sunshines = outputpath / "sunshines-v3.jsonl"
    outfile = outputpath / "sunshines-final.csv"
    if outfile.exists():
        print("file already exists")
        return

    schema = [
        "name",
        "sex",
        "paper_count",
        "citation_count",
        "h_index",
        "role_2020",
        "salary_2020",
        "benefits_2020",
        "role_2021",
        "salary_2021",
        "benefits_2021",
        "role_2022",
        "salary_2022",
        "benefits_2022",
        "role_2023",
        "salary_2023",
        "benefits_2023",
    ]

    with open(outfile, "w") as f:
        writer = csv.writer(f)
        writer.writerow(schema)

        for line in tqdm(open(sunshines, "r"), total=len(open(sunshines, "r").readlines())):
            employee = json.loads(line)

            def get_sex(name: str) -> Optional[str]:
                preds = gender_classifier(name)
                top1 = sorted(preds, key=lambda x: x["score"], reverse=True)[0]["label"]
                if top1 not in ["Male", "Female"]:
                    return None
                # check if string is "Male"
                if "Male" is top1:
                    return "M"
                return "F"

            def get_year(year: int):
                year_dic = [elem for elem in employee["years"] if elem["year"] == year]
                if len(year_dic) == 0:
                    return {
                        f"role_{year}": None,
                        f"salary_{year}": None,
                        f"benefits_{year}": None,
                    }
                year_dic = year_dic[0]
                return {
                    f"role_{year}": year_dic["role"],
                    f"salary_{year}": year_dic["salary"],
                    f"benefits_{year}": year_dic["benefits"],
                }

            fullname = employee["lastname"] + " " + employee["firstname"]
            fullname = " ".join([elem.lower().capitalize() for elem in fullname.split()])
            new_employee = {
                "name": fullname,
                "sex": get_sex(fullname),
                "paper_count": employee["paperCount"],
                "citation_count": employee["citationCount"],
                "h_index": employee["hIndex"],
                **get_year(2020),
                **get_year(2021),
                **get_year(2022),
                **get_year(2023),
            }

            for key in new_employee:
                if isinstance(new_employee[key], str):
                    new_employee[key] = new_employee[key].encode("ascii", "ignore").decode()

            writer.writerow([new_employee[key] for key in schema])


get_final()
