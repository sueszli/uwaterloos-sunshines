stuff i've done in chronological order:

- downloaded csrankings data
    - source: https://github.com/emeryberger/CSrankings/blob/gh-pages/csrankings.csv
    - schema: name,affiliation,homepage,scholarid
    - quarterly updated data, scholars can add pull requests to update their affiliation
- scraped uwaterloo's sunshine salary disclosure list for 2020-2023
    - converted html to csv
    - dropped unnecessary nested span tags
    - validated csv schema
- validated all csv files with csvlint (cli tool)
