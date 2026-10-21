# SpaceX Falcon 9 First-Stage Landing Prediction

**IBM Applied Data Science Capstone** · Martim Ramos

SpaceX prices a Falcon 9 launch at about $62 M, while other providers charge upwards of $165 M. Most of the difference comes from reusing the first stage. This project predicts whether the first stage will land successfully, which in turn helps estimate the cost of a launch.

📄 **Final report:** [Data Science Capstone Project Report.pdf](Data%20Science%20Capstone%20Project%20Report.pdf)

## Notebooks and files

| # | Lab | File |
|---|-----|------|
| 1 | Data collection: SpaceX REST API | [01_spacex_data_collection_api.ipynb](01_spacex_data_collection_api.ipynb) |
| 2 | Data collection: web scraping (Wikipedia) | [02_spacex_webscraping.ipynb](02_spacex_webscraping.ipynb) |
| 3 | Data wrangling | [03_spacex_data_wrangling.ipynb](03_spacex_data_wrangling.ipynb) |
| 4 | EDA with SQL | [04_spacex_eda_sql.ipynb](04_spacex_eda_sql.ipynb) |
| 5 | EDA with data visualization | [05_spacex_eda_dataviz.ipynb](05_spacex_eda_dataviz.ipynb) |
| 6 | Interactive map with Folium | [06_spacex_launch_site_location_folium.ipynb](06_spacex_launch_site_location_folium.ipynb) |
| 7 | Plotly Dash dashboard | [07_spacex_dash_app.py](07_spacex_dash_app.py) |
| 8 | Machine learning prediction | [08_spacex_machine_learning_prediction.ipynb](08_spacex_machine_learning_prediction.ipynb) |

The datasets are in [`data/`](data).

## Key results

- 90 Falcon 9 launches (2010–2020). **66.7%** landed, and the success rate rose from 0% (2010–13) to 90% (2019).
- KSC LC-39A has the best launch success ratio: **76.9%** (10 of 13).
- Orbits ES-L1, GEO, HEO and SSO had 100% success (few launches). GTO is the hardest, at 52%.
- Logistic Regression, SVM and KNN all reach **83.3%** test accuracy. **SVM** is the best model (84.8% CV accuracy, 84.8% ± 7.3% under repeated CV).

## Run it

```bash
pip install -r requirements.txt
jupyter lab                    # run the notebooks in order
python 07_spacex_dash_app.py   # dashboard at http://127.0.0.1:8050
```
