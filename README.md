# MLB Scraper Pitcher Data

This is a Python script that utilizes a MLB Scraper module by [Tnestico](https://github.com/tnestico/mlb_scraper) to retrieve and analyze pitcher data from the MLB Stats API. The data is processed and returned as Polars DataFrames, which are then converted into Pandas DataFrames for easy manipulation and analysis. 

Largely inspired by [Tnestico's Pitching Summary project](https://github.com/tnestico/pitching_summary), I wanted to focus on specific pitcher statistics, such as their types of pitches, each pitch type's velocity, spin rate, usage, max exit velocity, and more.

## Features
* Scrapes detailed pitcher data for a specific game using the 'MLB_Scrape' class.
* Processes and calculates advanced pitcher statistics such as:
	* Vertical and Horizontal Approach Angles (VAA, HAA)
	* Spin Rate, Average Velocity, Extension
	* Whiff percentage, Chase percentage, and Zone percentage
	* Induced vertical break (iVB) and Horizontal Break (HB)
* Outputs a comprehensive DataFrame with statistics per pitch type, including pitch counts, usage percentages, and whiff rates.  