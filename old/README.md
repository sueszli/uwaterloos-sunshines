_how it was built:_

-   get salary data ✅

    -   scrape uwaterloo public sector salary disclosure (sunshine list) for the years 2021 and 2022 ✅
    -   create a new "merged list" that contains all 2022 entries, as well as all 2021 entries that are missing in the 2022 list ✅

-   get the researcher's performance data ✅

    -   a) use google scholar search → i got IP blocked ❌
    -   b) use csrankings → failures: 1122/2051 (54%) ❌
    -   c) use the semantic scholar api → failures: 0417/2051 (20%) ✅

-   join salary table with the researcher's performance table ✅

-   find correlation and visualize data from the joined table → parallel coordinates plot ✅
