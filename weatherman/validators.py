from datetime import date

from constants import DEFAULT_VALUE, DATE_YEAR_INDEX, DATE_MONTH_INDEX, DATE_DAY_INDEX


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
            date_parts = date_str.replace("/", "-").split("-")
            parsed_date = date(
                int(date_parts[DATE_YEAR_INDEX]),
                int(date_parts[DATE_MONTH_INDEX]),
                int(date_parts[DATE_DAY_INDEX]),
            )
        except (ValueError, IndexError):
            parsed_date = None

    return parsed_date
