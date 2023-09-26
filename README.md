> keep in mind: after processing, the repository must go private, the data must be obfuscated and the page should be only accessible on github pages with a little password

<br><br><br>

steps:

-   get salary data ✅

    -   scrape uwaterloo public sector salary disclosure (sunshine list) for the years 2021 and 2022 ✅
    -   create a new "merged list" that contains all 2022 entries, as well as all 2021 entries that are missing in the 2022 list ✅

-   get performance data ✅

    -   a) use google scholar search → i got IP blocked ❌
    -   b) use csrankings → failures: 1122/2051 (54%) ❌
    -   c) use the semantic scholar api → failures: 0417/2051 (20%) ✅

-   join the two tables [name, salary, scraped data from semantic scholar]

-   find correlation between salary and publication count
