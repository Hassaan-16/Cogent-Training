"""constants to be used throughout weatherman"""

# local_parser.py
COLUMNS_TO_READ = [
    0,
    1,
    3,
    7,
    9,
]  # date, max_temp, min_temp, max_humidity, mean_humidity
FILE_NAME_FORMAT = "Murree_weather_{year}_{month}.txt"

# reports.py console chart colors
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
