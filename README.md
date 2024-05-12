## aggregation-isinholder-position-for-hfintv

# FCA Short Positions Scraper and Aggregator

This Python script scrapes the FCA website for disclosed short positions and calculates aggregated data by ISIN and historical date. The script then stores the output in a SQLite database table.

# Objective
The script aims to provide aggregated information on disclosed short positions, including the total percentage short and the total number of funds disclosed, for each ISIN and historical date.

# Assumptions
If a disclosure is made on a specific date, the position remains the same until there is a new disclosure by the same holder.
If there are no further disclosures by the same holder, the assumption is that the disclosure closes on the following business date.
Dates are reindexed to business days (Monday to Friday).


# Notes
The script only uses data from the historic disclosures sheet on the FCA website.
Ensure that you have proper internet connectivity to scrape data from the FCA website.
The script should be run periodically to keep the data up-to-date.

# References
Financial Conduct Authority (FCA) website
https://www.fca.org.uk/publication/data/

# SQLite
https://docs.python.org/3/library/sqlite3.html
Feel free to modify the script and adapt it to your specific requirements. If you encounter any issues or have suggestions for improvement, please let me know!
