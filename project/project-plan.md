# Project Plan

## Comparison of life expectancy in the countries of the Americas

Awesome MADE project.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How has life expectancy developed over the last 20 years in the various countries of North and South America?
2. are there clear differences to the growth of the economy?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
This project aims to answer two questions. 
Firstly, it analyzes how life expectancy has developed in the countries of North and South America over the last 20 years. 
Selected countries will be compared to identify differences and similarities in the development of life expectancy. 
If complete data is not available for all countries, the analysis will focus on the countries with the most reliable data sets.

Secondly, the project goes one step further and analyzes whether economic growth has an influence on the development of life expectancy. 
By analyzing economic indicators (such as GDP growth) in conjunction with life expectancy data, the project will explore whether there is a discernible link between economic progress and improvements in life expectancy.

The results of this project will provide a better understanding of how social and economic conditions affect life expectancy in the Americas and whether economic prosperity automatically leads to longer lives.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Life Expectancy Data
* Data URL: https://data.un.org/Data.aspx?d=PopDiv&f=variableID%3a68
* Data Type: CSV

The 2024 Revision of World Population Prospects represents the latest global set of demographic estimates and projections prepared by the Population Division of the Department of Economic and Social Affairs of the United Nations Secretariat. It displays key demographic indicators for selected periods or dates from 1950 to 2100, for the world, development groups, regions, subregions, and countries or areas with more than 1,000 inhabitants in 2023. For countries or areas with fewer than 1,000 inhabitants in 2023, only figures related to population size and growth are provided. The estimates and projections contained in this revision cover a 150-year time horizon, which can be subdivided into estimates (1950-2023) and projections (2024-2100).
(Cite from the data source)

### Datasource2: GDP Data
* Data URL: https://data.un.org/Data.aspx?d=SNAAMA&f=grID%3a101%3bcurrID%3aUSD%3bpcFlag%3a1
* Data Type: CSV

The Economic Statistics Branch of the United Nations Statistics Division (UNSD) maintains and annually updates the National Accounts Main Aggregates database. It consists of a complete and consistent set of time series, from 1970 onwards, of the main National Accounts aggregates of all UN Members States and other territories in the world for which National Accounts information is available. Its contents are based on the official data reported to UNSD through the annual National Accounts Questionnaire, supplemented with data estimates for any years and countries with incomplete or inconsistent information.
(Cite from the data source)

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Analysis of the data [#1][i1]
2. Creating data pipelines [#2][i2]
3. Visualization of the data [#3][i3]
4. ....

[i1]: https://github.com/jvalue/made-template/issues/1