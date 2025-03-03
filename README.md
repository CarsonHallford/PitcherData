# MLB Scraper Pitcher Data

This is a Python script that utilizes a MLB Scraper module by [Tnestico](https://github.com/tnestico/mlb_scraper) to retrieve and analyze pitcher data from the MLB Stats API. The data is processed and returned as Polars DataFrames, which are then converted into Pandas DataFrames for easy manipulation and analysis. 

Largely inspired by [Tnestico's Pitching Summary project](https://github.com/tnestico/pitching_summary) I wanted to focus on specific pitcher statistics, such as their types of pitches, each pitch type's velocity, spin rate, usage, max exit velocity, and more.