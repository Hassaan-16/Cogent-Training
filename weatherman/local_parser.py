import csv
import calendar
import data_models
from pathlib import Path
from datetime import date
from constants import (
    COLUMN_KEY_DATE,
    COLUMN_KEY_MAX_TEMP,
    COLUMN_KEY_MIN_TEMP,
    COLUMN_KEY_MAX_HUMIDITY,
    COLUMN_KEY_MEAN_HUMIDITY,
    DATE_YEAR_INDEX,
    DATE_MONTH_INDEX,
    DATE_DAY_INDEX,
    MONTH_FIRST_INDEX,
    MONTH_LAST_INDEX,
    FILE_NAME_FORMAT,
)


class WeatherParser:
    """Handles discovery and parsing of weather CSV files."""

    def __init__(self, directory_path):
        self.directory_path = Path(directory_path)

    @staticmethod
    def _safe_float(raw_string_value):
        """Converts a string to a float, safely returning None for missing or invalid data."""
        if raw_string_value and str(raw_string_value).strip() not in ("", "None"):
            return float(str(raw_string_value).strip())

        return None

    @staticmethod
    def _safe_date(date_str):
        """SRP Helper: Exclusively parses and validates dates at the boundaries."""
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

    def _extract_raw_rows(self, filename):
        """Handles File I/O: Reads a CSV file using DictReader and returns the valid raw rows."""
        raw_weather_rows = []
        file_path_object = Path(filename)

        try:
            with file_path_object.open("r", encoding="utf-8") as weather_file_readings:
                weather_file_readings = csv.DictReader(weather_file_readings)

                for file_reading in weather_file_readings:
                    if (
                        file_reading.get(COLUMN_KEY_DATE)
                        and file_reading.get(COLUMN_KEY_DATE).strip()
                    ):
                        raw_weather_rows.append(file_reading)

        except OSError as error:
            print(f"Error reading file: {filename}\nException: {error}")

        return raw_weather_rows

    def _build_weather_readings(self, raw_weather_rows):
        """Handles Data Modeling: Converts raw CSV dict rows into WeatherReading objects."""
        parsed_readings = []

        for weather_readings in raw_weather_rows:
            date_value = self._safe_date(
                weather_readings.get(COLUMN_KEY_DATE, "").strip()
            )

            if date_value:
                weather_reading = data_models.WeatherReading(
                    date=date_value,
                    maximum_temperature=self._safe_float(
                        weather_readings.get(COLUMN_KEY_MAX_TEMP)
                    ),
                    minimum_temperature=self._safe_float(
                        weather_readings.get(COLUMN_KEY_MIN_TEMP)
                    ),
                    maximum_humidity=self._safe_float(
                        weather_readings.get(COLUMN_KEY_MAX_HUMIDITY)
                    ),
                    mean_humidity=self._safe_float(
                        weather_readings.get(COLUMN_KEY_MEAN_HUMIDITY)
                    ),
                )
                parsed_readings.append(weather_reading)

        return parsed_readings

    def _file_parse(self, filepath):
        """Coordinates parsing a single weather file into WeatherReading objects."""
        raw_weather_rows = self._extract_raw_rows(filepath)

        return self._build_weather_readings(raw_weather_rows)

    @staticmethod
    def _generate_file_pattern(target_period):
        """Generates the glob search pattern from the user's target period string."""
        date_parts = target_period.split("/")
        target_year = date_parts[DATE_YEAR_INDEX]

        if len(date_parts) <= DATE_MONTH_INDEX:
            file_pattern = FILE_NAME_FORMAT.format(year=target_year, month="*")
        else:
            try:
                month_num = int(date_parts[DATE_MONTH_INDEX])

                if not MONTH_FIRST_INDEX <= month_num <= MONTH_LAST_INDEX:
                    print(
                        f"Error: Invalid month '{month_num}'. Please use a value between 1 and 12."
                    )

                    return None

                month_abbr = calendar.month_abbr[month_num]
                file_pattern = FILE_NAME_FORMAT.format(
                    year=target_year, month=month_abbr
                )

            except ValueError:
                print(f"Error: Invalid month format in '{target_period}'.")

                return None

        return file_pattern

    def parse_period(self, target_period):
        """Schedules file parsing by locating files that match the requested period."""
        all_weather_readings = []

        file_pattern = self._generate_file_pattern(target_period)
        if not file_pattern:
            return []

        matching_files = list(self.directory_path.glob(file_pattern))

        if not matching_files:
            print(f"No data files found matching pattern: {file_pattern}")
        else:
            for filepath in matching_files:
                all_weather_readings.extend(self._file_parse(filepath))

        return all_weather_readings
