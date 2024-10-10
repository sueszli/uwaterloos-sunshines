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
- merged all sunshine files into one
    - cleaned strings
    - employees have multiple entries, so it's timeseries data
- merged csrankings with sunshine list
    - used fuzzy matching to match names, dropped non uwaterloo affiliations
    - very few matches, so i'll have to use semantic scholar api + google scholar api
        - num all rows in csrankings: 29360
        - num uwaterloo rows csranking: 149
        - num all rows in sunshines: 2514
        - found matches: 107 (using threshold 0.8 - anything else would lead to duplicates)
- failed joining with google scholar
    - got ip blocked, doesn't have an api meant for information retrieval
    - other related proxy services are pretty expensive
    - endpoint: `https://scholar.google.com/citations?view_op=search_authors&mauthors=`
- joined with semantic scholar
    - endpoint: `https://api.semanticscholar.org/graph/v1/author/search?query=`



<!-- 
-   b) use csrankings → failures: 1122/2051 (54%) ❌
-   c) use the semantic scholar api → failures: 0417/2051 (20%) ✅

-   join salary table with the researcher's performance table ✅

-   find correlation and visualize data from the joined table → parallel coordinates plot ✅

-->
