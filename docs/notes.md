stuff i've done in chronological order:

1) scrape uwaterloo's sunshine list for 2020-2023

- converted html to csv using beautifulsoup
- dropped unnecessary nested span tags
- validated csv schema
- merged all sunshine files into one (partially as timeseries data in jsonl format)
- cleaned strings
- validated all csv files with csvlint (cli tool)

2) downloaded csrankings data and merged with sunshine list

- source: https://github.com/emeryberger/CSrankings/blob/gh-pages/csrankings.csv
- schema: name,affiliation,homepage,scholarid
- quarterly updated data, scholars can add pull requests to update their affiliation
- used fuzzy matching to match names, dropped non uwaterloo affiliations
- very few matches
    - num all rows in csrankings: 29360
    - num uwaterloo rows csranking: 149
    - num all rows in sunshines: 2514
    - found matches: 107 (using threshold 0.8 - anything else would lead to duplicates) -> meaning 107/149 csrankings matched with sunshine list which is not bad
- stored an `csrankings_scholarids` field that is completely useless

3) failed joining with google scholar

- endpoint: `https://scholar.google.com/citations?view_op=search_authors&mauthors=`
- got ip blocked, doesn't have an api meant for information retrieval
- other related proxy services are pretty expensive

4) joined with semantic scholar

- endpoint: `https://api.semanticscholar.org/graph/v1/author/search?query=`
- switching ips via vpn was helpful
- fields:
    - `affiliations` field was always empty although that would have been most useful
    - `homepage` field was also alwyas empty
- searched for researchers via api
    - filtered by fuzzy name matching (threshold 0.8)
    - filtered by options with external ids (if there were any) like dblp, orcid, etc.
    - took the option with the highest combined citation count, paper count, h-index → this definitely leads to some errors but it's the best heuristic i could come up with
- new fields:
    - `authorId` (to look up more stuff via the semantic scholar api)
    - `externalIds`: ie. mostly dblp if there are any (useless)
    - `name`: the name we matched with (useless)
    - `paperCount`, `citationCount`, `hIndex`
    - there are no other fields we could check
- data loss
    - only 1708/2514 (68%) of employees could be joined with semantic scholar
    - not all of that is data loss, because some employees are not researchers

5) preprocessing

- we have joined: sunshines x csrankings x semantic scholar data
- converting jsonl to csv to speed up queries
- dropped unnecessary fields
- inferred sex with some distilbert model

6) analysis

...
