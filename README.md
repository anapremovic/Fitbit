# Fitbit Data Analysis

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
        <ul><li><a href="#built-with">Built With</a></li></ul>
    </li>
    <li>
		<a href="#installation">Installation</a>
		<ul>
			<li><a href="#manually">Manually</a></li>
			<li><a href="#automatically">Automatically</a></li>
		</ul>
    </li>
    <li>
		<a href="#usage">Usage</a>
        <ul>
        	<li><a href='#folder-dashboard'>Folder: Dashboard</a></li>
		</ul>
        <ul>
			<li><a href='#folder-part1-4'>Folder: Parts 1 - 4</a></li>
			<ul><li><a href="#part-1">Part 1</a></li></ul>
			<ul><li><a href="#part-2">Part 2</a></li></ul>
			<ul><li><a href="#part-3">Part 3</a></li></ul>
			<ul><li><a href="#part-4">Part 4</a></li></ul>
        </ul>
    </li>
    <li><a href="#notes">Notes</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

This is a study of data from an Amazon survey from 2016 of 30 respondents. We perform an analysis and visualize our results in a dashboard.

### Built With
[![Python][Python.org]][Python-url]
[![Streamlit][Streamlit.io]][Streamlit-url]
[![Plotly][Plotly.io]][Plotly-url]

## Installation

### Manually

1) Download [Python][Python-url] using version 3.10 at the minimum
2) This project uses a variety of Python libraries to run it. Please install the following:
  - [NumPy][NumPy-url]
  - [Pandas][Pandas-url]
  - [Streamlit][Streamlit-url]
  - [Streamlit's SQLAlchemy][Streamlit-SQLAlchemy-url]
  - [Plotly][Plotly-url]
3) Once you've completed the steps above, change your directory to the ***dashboard*** folder and run the command ``streamlit run fitbit_app.py``. This will start the dashboard and open it up on your local machine.
4) If you want to see the diagrams by themselves, navigate to the ***part1-4*** folder and run the command ``python main.py`` to see our visualizations from parts 1 to 4.

### Automatically

If you want to set up this dashboard yourself, please follow these steps:

1) Join Streamlit's [Community Cloud](https://streamlit.io/cloud?ref=blog.streamlit.io)
2) Create an account in the Community Cloud using your GitHub account
3) Once you're in the cloud's home page, press the **Create app** button to start this project as your dashboard.

## Usage

### Folder: Dashboard

This folder contains the visualizations and Streamlit code to display our FitBit dashboard. The *diagrams* folder holds Plotly charts containing certain charts pertaining to the page it is attached to (e.g. exercise diagrams show Plotly charts about exercise, health diagrams show Plotly charts about a user's health, etc.).

The ``[page_name]_page.py`` files contain the pages the user can navigate to on the dashboard, and our home screen can be found in the ``fitbit_app.py`` file.

### Folder: Part1-4

This folder contains the functions for each individual graph listed in the bullet points for parts 1 to 4 found in the minimal requirements on Canvas.1

#### Part 1
* Visualize distance travelled by users.
* Visualize calories burnt per user.
* Visualize frequency of workout per day of week.
* Visualize relationship between the amount of steps taken and the amount of calories burnt.

#### Part 2
* View repository and README.

#### Part 3
* Verify correctness of hourly steps vs daily steps data.
* Visualize sleep data over time for a user.
* Visualize relationship between the amount of sleep and the number of active minutes the next day.
* Visualize a given user's heart rate and intensity side-by-side, as well as their average heart rate and intensity.
* Visualize the correlation of the rate of activity between temperature, precipitation, total distance and calories burned.

#### Part 4
* Compare how relationship between the amount of sleep and the number of active minutes changes on weekdays vs weekends.
* Visualize relationship between the number of steps in a day and the average daily heart rate.
* Numerically see the average daily heart rate for a given step range.

## Notes

- The daily step data isn't completely correct as it does not match the hourly step data

## Contributors

* Alec Rothkowitz
* Ana Premovic
* Lucas Lee
* Luke Olender

## Acknowledgments

* <a href="https://github.com/othneildrew/Best-README-Template">README Template</a>

[Python-url]: https://www.python.org/

<!-- Shields.io badges -->
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&size=150
[Streamlit.io]: https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&size=150
[Plotly.io]: https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=fff&style=for-the-badge

<!-- Python libraries -->
[NumPy-url]: https://numpy.org/
[Pandas-url]: https://pandas.pydata.org/
[Streamlit-url]: https://streamlit.io/
[Streamlit-SQLAlchemy-url]: https://docs.streamlit.io/develop/concepts/connections/connecting-to-data
[Plotly-url]: https://plotly.com/