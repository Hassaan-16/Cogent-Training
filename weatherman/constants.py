"""constants to be used throughout weatherman"""

DEFAULT_VALUE = 0.0
DATE_YEAR_INDEX = 0
DATE_MONTH_INDEX = 1
DATE_DAY_INDEX = 2
DATE_PARTS_LIMIT = 3

MONTH_FIRST_INDEX = 1
MONTH_LAST_INDEX = 12

MINIMUM_VALUE = 0

RED_ASCII = "\033[91m"
BLUE_ASCII = "\033[94m"
RESET_ASCII = "\033[0m"

MAX_TEMP = "maximum_temperature"
MIN_TEMP = "minimum_temperature"
MAX_HUMIDITY = "maximum_humidity"
MEAN_HUMIDITY = "mean_humidity"

COLUMN_KEY_DATE = "PKT"
COLUMN_KEY_MAX_TEMP = "Max TemperatureC"
COLUMN_KEY_MIN_TEMP = "Min TemperatureC"
COLUMN_KEY_MAX_HUMIDITY = "Max Humidity"
COLUMN_KEY_MEAN_HUMIDITY = " Mean Humidity"

FILE_NAME_FORMAT = "Murree_weather_{year}_{month}.txt"

LABEL_HIGHEST = "Highest"
LABEL_LOWEST = "Lowest"
LABEL_HUMIDITY = "Humidity"

UNIT_CELSIUS = "C"
UNIT_PERCENT = "%"

NOT_APPLICABLE = "N/A"
UNKNOWN = "Unknown"

CLI_DESCRIPTION = "weatherman CLI weather analyser"
ARG_FILEPATH = "filepath"
HELP_FILEPATH = "path to the file directory"

FLAG_AVERAGE = "-a"
FLAG_BONUS = "-b"
FLAG_CHART = "-c"
FLAG_EXTREME = "-e"

DEST_AVERAGE = "average_month"
DEST_BONUS = "bonus_month"
DEST_CHART = "chart_month"
DEST_EXTREME = "extreme_year"

HELP_AVERAGE = "year/month for average values report"
HELP_BONUS = "Year/Month for the bonus chart"
HELP_CHART = "year/month chart values report"
HELP_EXTREME = "Year for extreme values report"
