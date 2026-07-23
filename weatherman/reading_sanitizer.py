from datetime import date

from constants import DEFAULT_VALUE


class ReadingSanitizer:
    """Helper class containing static utility functions for parsing weather data."""

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
