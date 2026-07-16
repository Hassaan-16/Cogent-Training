from calendar import month_abbr
from datetime import date

from constants import (
    DEFAULT_VALUE,
    DATE_YEAR_INDEX,
    DATE_MONTH_INDEX,
    DATE_DAY_INDEX,
    MONTH_FIRST_INDEX,
    MONTH_LAST_INDEX,
    FILE_NAME_FORMAT,
)


def generate_file_pattern(target_period):
    """Generates the glob search pattern from the user's target period string."""
    date_parts = target_period.split("/")
    target_year = date_parts[DATE_YEAR_INDEX]

    if len(date_parts) <= DATE_MONTH_INDEX:
        file_pattern = FILE_NAME_FORMAT.format(year=target_year, month="*")
    else:
        try:
            month_num = int(date_parts[DATE_MONTH_INDEX])
        except ValueError:
            print(f"Error: Invalid month format in '{target_period}'.")

            return None

        if not MONTH_FIRST_INDEX <= month_num <= MONTH_LAST_INDEX:
            print(
                f"Error: Invalid month '{month_num}'. Please use a value between 1 and 12."
            )

            return None

        month_abbreviation = month_abbr[month_num]
        file_pattern = FILE_NAME_FORMAT.format(
            year=target_year, month=month_abbreviation
        )

    return file_pattern


def convert_to_float(raw_string_value):
    """Converts a string to a float, safely returning None for missing or invalid data."""
    if raw_string_value and str(raw_string_value).strip() not in ("", "None"):
        return float(str(raw_string_value).strip())

    return None


def handle_missing_values(weather_value):
    """safely handle any missing daily data values."""

    return weather_value if weather_value is not None else DEFAULT_VALUE


def validate_date(date_str):
    """Exclusively parses and validates dates at the boundaries."""
    parsed_date = None
    if date_str:
        try:
            parts = date_str.replace("/", "-").split("-")
            parsed_date = date(
                int(parts[DATE_YEAR_INDEX]),
                int(parts[DATE_MONTH_INDEX]),
                int(parts[DATE_DAY_INDEX]),
            )
        except (ValueError, IndexError):
            parsed_date = None

    return parsed_date
