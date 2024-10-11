---
title: "Lab Report"
subtitle: "186.868 Visual Data Science 2024W"
author: "11912007 - Yahya Jabary"
documentclass: article
papersize: a4
fontsize: 10pt
geometry:
    - top=10mm
    - bottom=15mm
    - left=10mm
    - right=10mm
toc: true
---

This report contains the contents of all tasks to be completed in the laboratory section of this course. The individual subtasks are described in seperate sections.

# Requirements

The following requirements have been met in this project.

Topic Selection:

- [x] Either select one of the suggested topics, or come up with your own idea. → Our custom topic was confirmed by the lecturer via email.
- [x] The topic should be possible to easily understand the data context, even if you are not an expert.

Discover:

- [x] Use at least two independent datasets. → We joined 6 datasets, 3 of which are independent.
- [x] The selected datasets must be multidimensional: they have to contain more than 5 variables. → The final joined table has 14 features.
- [x] The selected datasets must contain a sufficient amount of data rows. → The final joined table has ~2k rows but the original datasets have ~30k rows.

Prerequisites:

- [x] The lab part has to be solved using a charting library. Fully-featured applications are not allowed to be used.


# Discover

The tasks of this section are:

- Discover your topic
- Describe the two datasets you selected
- Implicit: define questions to answer with the data
- Keep the length to 1-2 A4 pages

<!--

It's very rare for academic institutions to disclose the salaries of their employees, especially with identifying information. The University of Waterloo has been publishing the salaries of its top earning employees, earning more than $100k (a.k.a. the "Sunshine List") since 1957.

Disclaimer: I studied there.

By using the employee

-->

# Wrangle

The tasks of this section are:

- Join the two or more datasets you selected into one big data table
    - How did you join the datasets? Which keys did you use to join the data? Did all keys match? Did you have to introduce new keys?
- Solve issues like formatting issues, missing data, faulty values, and non-matching keys.
    - Which data cleaning steps have been necessary? Did you experience data issues, and if so, which ones? How did you solve them? Did you use automated methods? Did you use visualization to inspect data issues?
- Visually show and explain the data quality of your dataset (for example, before and after cleaning steps). Come up with your own, creative, solution here.
- Keep the length to 3/4 to 1 A4 page.

# Profile

In this section we explore the data in detail, to completely understand its structure, and to discover any interesting patterns that can be found in there.

The tasks of this section are:

- Find at least 3 informative insights in your dataset. For each one add a short text describing the insights plus one visualization.
- Keep the length to 3/4 to 1 A4 page per insight.

# Model

The tasks of this section are:

- Build a model of the data you studied, to find answers to the questions you selected (possible models: linear regression, clustering, pca, anomaly detection, etc.)
- describe the modeling process
- Create one or more visualization(s) that describe the results of your model
    - How would you increase trust of your customers/colleagues in your modeling approach by using data visualization?
- Keep the length to 1-2 A4 pages.

# Report

The tasks of this section are:

- Show your findings in an interactive dashboard to a broader audience. The findings may be related to the Model/Wrangle/Profile stages.
    - Use appropriate charts, visual encodings (e.g., color).
    - Use at least four different types of visualizations / charts.
    - Include interaction (e.g., filters, zoom, not a jupyter notebook), brushing & linking (changes in one view affect others, but not global filters)
- See examples: https://tuwel.tuwien.ac.at/mod/page/view.php?id=2433356
