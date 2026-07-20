from calendar import month_abbr
from datetime import date

from constants import (
    DATE_MONTH_INDEX,
    DATE_YEAR_INDEX,
    DEFAULT_VALUE,
    FILE_NAME_FORMAT,
    MONTH_FIRST_INDEX,
    MONTH_LAST_INDEX,
)


class WeatherParserUtility:
    """Helper class containing static utility functions for parsing weather data."""

    @staticmethod
    def _get_month_abbreviation(month_string, full_target_period):
        """Validates the month and converts it to its calendar abbreviation."""
        try:
            month_num = int(month_string)
        except ValueError:
            print(f"Error: Invalid month format in '{full_target_period}'.")

            return None

        if not MONTH_FIRST_INDEX <= month_num <= MONTH_LAST_INDEX:
            print(
                f"Error: Invalid month '{month_num}'. "
                "Please use a value between 1 and 12."
            )

            return None

        return month_abbr[month_num]

    @staticmethod
    def _extract_date_parts(target_period):
        """Extracts the year and optional month from the period string."""
        date_parts = target_period.split("/")
        target_year = date_parts[DATE_YEAR_INDEX]

        if len(date_parts) <= DATE_MONTH_INDEX:
            return target_year, None

        return target_year, date_parts[DATE_MONTH_INDEX]

    @staticmethod
    def generate_file_pattern(target_period):
        """Generates the glob search pattern from the user's target period string."""
        target_year, target_month = WeatherParserUtility._extract_date_parts(
            target_period
        )

        if not target_month:
            return FILE_NAME_FORMAT.format(year=target_year, month="*")

        month_abbreviation = WeatherParserUtility._get_month_abbreviation(
            target_month, target_period
        )

        if not month_abbreviation:
            return None

        return FILE_NAME_FORMAT.format(year=target_year, month=month_abbreviation)

    @staticmethod
    def validate_date(date_str: str | None) -> date | None:
        """Parse a date string in YYYY-MM-DD or YYYY/MM/DD format."""
        try:
            year, month, day = map(int, date_str.replace("/", "-").split("-"))

            return date(year, month, day)

        except (ValueError, IndexError):
            return None

    @staticmethod
    def convert_to_float(raw_string_value):
        """Converts a string to float, safely returning None for missing data."""
        if raw_string_value and str(raw_string_value).strip() not in ("", "None"):
            return float(str(raw_string_value).strip())

        return None

    @staticmethod
    def handle_missing_values(weather_value):
        """safely handle any missing daily data values."""

        return weather_value if weather_value is not None else DEFAULT_VALUE
