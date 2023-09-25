steps:

-   get salary data [name, salary] ✅

    -   scrape uwaterloo public sector salary disclosure (sunshine list) for the years 2021 and 2022 ✅
    -   create a new "merged list" that contains all 2022 entries, as well as all 2021 entries that are missing in the 2022 list ✅

-   get google scholar link for each name [name, google scholar link]

    -   a) use google scholar search → got me IP blocked, even after paying for a proxy service - not feasible ❌
    -   b) use csrankings → low hit rate on the sunshine list (sub 50%) – inaccurate ❌
    -   c) semantic scholar (gets paid for by my course) → https://api.semanticscholar.org/api-docs/graph#tag/Author-Data/operation/get_graph_get_author_search

-   join the two lists [name, salary, scraped data from google scholar]

-   find correlation between salary and publication count
