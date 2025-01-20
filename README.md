# Analysing the relationship between gross domestic product per capita (growth) and life expectancy (growth) in countries in the Americas

## Overview
Over the years, economic power has increased in all countries. Due to medical progress over the years, this also applies to life expectancy in most countries. The higher the economic power, the higher the life expectancy, presumably because there is enough money available for high-tech medical treatments, which can be used to treat diseases in old age in particular.

However, the exact nature of this correlation is unclear. More precisely, what influence the gross domestic product per capita has on life expectancy. It is clear that it cannot be linear, as exponential economic growth has already been observed in the past, but this does not have such a one-to-one effect on life expectancy. For this reason, the influence of growth in gross domestic product per capita on growth in life expectancy is analysed below by comparing it for wealthy, middle-income and poor countries.

## Data Sources
|             | Data Source                                                                                                                               | Data Source                                                                                                                 | Data Source                                                                                                                                      |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Title       | Life expectancy at birth (years)                                                                                                          | Gross domestic product per capita                                                                                           | Gross domestic product per capita                                                                                                                |
| Data-URL    | [World Bank Life expectancy at birth (years)](https://genderdata.worldbank.org/en/indicator/sp-dyn-le00-in?gender=total)                  | [World Bank](https://data.worldbank.org/)                                                                                   | [World Bank GDP per capita](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)                                                                 |
| License     | [CC-BY-4.0](https://datacatalog.worldbank.org/public-licenses#cc-by)                                                                      | [CC-BY-4.0](https://datacatalog.worldbank.org/public-licenses#cc-by)                                                        | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)                                                                                  |
| Description | The CSV file contains information on life expectancy for all countries in the world from 1960 to 2022, divided into men, women and total. | The data set contains the gross domestic product per capita for all countries in the world in the period from 1960 to 2023. | This dataset contains information on the country names and country codes in connection with the continent on which these countries are located.  |

## Requirements

- Python 3
- Jupyter Notebook
- Pandas
- Matplotlib
- Numpy

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/fi51wate/made.git
   ```
2. Go to directory
   ```sh
   cd made
   ```
3. Download the data
   ```sh
   ./pipeline.sh
   ```
4. Optionally validate the downloaded data:
   ```sh
   ./test.sh
   ```
5. Run the Jupyter Notebook `project/project.ipynb`

## Further Links

- Link to the Jupyter Notebook: [project.ipynb](https://github.com/fi51wate/made/blob/main/project/project.ipynb)
- Link to the Final Report: [analysis-report.pdf](https://github.com/fi51wate/made/blob/main/project/analysis-report.pdf)
- Link to the Data Quality Report: [data-report.pdf](https://github.com/fi51wate/made/blob/main/project/data-report.pdf)
