# Fitbit Data Analysis

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
        <ul><li><a href="#built-with">Built With</a></li></ul>
    </li>
    <li>
		<a href="#getting-started">Getting Started</a>
    </li>
    <li>
		<a href="#project-structure">Project Structure</a>
        <!-- <ul>
        	<li><a href='#folder-dashboard'>Folder: Dashboard</a></li>
		</ul>
        <ul>
			<li><a href='#folder-part1-4'>Folder: Parts 1 - 4</a></li>
			<ul><li><a href="#part-1">Part 1</a></li></ul>
			<ul><li><a href="#part-2">Part 2</a></li></ul>
			<ul><li><a href="#part-3">Part 3</a></li></ul>
			<ul><li><a href="#part-4">Part 4</a></li></ul>
        </ul> -->
    </li>
    <li><a href="#notes">Notes</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

This is a study of data from an Amazon survey from 2016 of 35 respondents. We perform an analysis and visualize our results in a dashboard.

Our data can be found at [Kaggle](https://www.kaggle.com/datasets/salihobaid/fitbit-datasets-0312201605122016/data) which is based on a research article called [Establishing Linkages Between Distributed Survey Responses and Consumer Wearable Device Datasets: A Pilot Protocol](https://doi.org/10.2196/resprot.6513) that aims to find a link between fitness trackers and an individual's physical activity.

The goal of our dashboard is to aid business analysts working for the manufacturer of Fitbit to improve their product. Participants of the study are also welcome to view the dashboard.

### Built With
[![Python][Python.org]][Python-url]
[![Streamlit][Streamlit.io]][Streamlit-url]
[![Plotly][Plotly.io]][Plotly-url]

## Getting Started

The recommended method is to access our dashboard directly: https://fitbit.streamlit.app/

If you want to run the dashboard on your local device, please follow these steps:

1) Download [Python][Python-url] using version 3.10 at the minimum
2) This project uses a variety of Python libraries to run it. We recommend using [pip](https://packaging.python.org/en/latest/key_projects/#pip) to get these packages onto your computer. A pip package is installed in the format: ``pip install package_name``. Please install the following:
  - [NumPy][NumPy-url]
  - [Pandas][Pandas-url]
  - [Statsmodels][Statsmodels-url]
  - [Streamlit][Streamlit-url]
  - [Streamlit's SQLAlchemy][Streamlit-SQLAlchemy-url]
  - [Plotly][Plotly-url]
3) Once you've completed the steps above, change your directory to the root folder and run the command ``streamlit run scripts/fitbit_app.py``. This will start the dashboard and open it up on your local machine.

## Project Structure

- The `scripts` directory contains `database.py` which contains database connection and all SQL queries, and fitbit_app.py which contains the global configuration for the Streamlit dashboard.
- The `scripts/diagrams` directory contains functions which generate Plotly diagrams pertaining to each dashboard page.
- The `scripts/app_pages` directory contains files to place the Plotly diagrams on each dashboard page.

## Notes

- Due to inconsistencies with the dataset we were given, the daily step data does not match the hourly step data

## Contributors

* Alec Rothkowitz
* Ana Premovic
* Lucas Lee
* Luke Olender

## Acknowledgments

* <a href="https://github.com/othneildrew/Best-README-Template">README Template</a>
* [Favicon](https://iconscout.com/free-icon/fitbit-3521429_2944873)
* [Logo](https://www.sherwoods.ie/fitbit/)

[Python-url]: https://www.python.org/

<!-- Shields.io badges -->
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&size=150
[Streamlit.io]: https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&size=150
[Plotly.io]: https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=fff&style=for-the-badge

<!-- Python libraries -->
[NumPy-url]: https://numpy.org/
[Pandas-url]: https://pandas.pydata.org/
[Statsmodels-url]: https://www.statsmodels.org/stable/index.html
[Streamlit-url]: https://streamlit.io/
[Streamlit-SQLAlchemy-url]: https://docs.streamlit.io/develop/concepts/connections/connecting-to-data
[Plotly-url]: https://plotly.com/