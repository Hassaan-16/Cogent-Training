import csv
from pathlib import Path

import data_models
from constants import (
    COLUMN_KEY_DATE,
    COLUMN_KEY_MAX_HUMIDITY,
    COLUMN_KEY_MAX_TEMP,
    COLUMN_KEY_MEAN_HUMIDITY,
    COLUMN_KEY_MIN_TEMP,
)
from weather_parser_utility import WeatherParserUtility


class WeatherParser:
    """Handles discovery and parsing of weather CSV files."""

    def __init__(self, directory_path):
        self.directory_path = Path(directory_path)

    def _extract_raw_rows(self, filename):
        """Reads a CSV file using DictReader and returns the valid raw rows."""
        raw_weather_rows = []
        file_path_object = Path(filename)

        try:
            with file_path_object.open("r", encoding="utf-8") as weather_file:
                weather_file_readings = csv.DictReader(weather_file)

                for file_reading in weather_file_readings:
                    if (
                        file_reading.get(COLUMN_KEY_DATE)
                        and file_reading.get(COLUMN_KEY_DATE).strip()
                    ):
                        raw_weather_rows.append(file_reading)

        except OSError as error:
            print(f"Error reading file: {filename}\nException: {error}")

        return raw_weather_rows

    def store_weather_readings(self, raw_weather_rows):
        """Converts raw CSV dict rows into cleanly validated WeatherReading objects."""
        parsed_readings = []

        for weather_readings in raw_weather_rows:
            date_value = WeatherParserUtility.validate_date(
                weather_readings.get(COLUMN_KEY_DATE, "").strip()
            )

            if date_value:
                weather_reading = data_models.WeatherReading(
                    date=date_value,
                    maximum_temperature=WeatherParserUtility.convert_to_float(
                        weather_readings.get(COLUMN_KEY_MAX_TEMP)
                    ),
                    minimum_temperature=WeatherParserUtility.convert_to_float(
                        weather_readings.get(COLUMN_KEY_MIN_TEMP)
                    ),
                    maximum_humidity=WeatherParserUtility.convert_to_float(
                        weather_readings.get(COLUMN_KEY_MAX_HUMIDITY)
                    ),
                    mean_humidity=WeatherParserUtility.convert_to_float(
                        weather_readings.get(COLUMN_KEY_MEAN_HUMIDITY)
                    ),
                )
                parsed_readings.append(weather_reading)

        return parsed_readings

    def _parse_file(self, filepath):
        """Coordinates parsing a single weather file into WeatherReading objects."""
        raw_weather_rows = self._extract_raw_rows(filepath)

        return self.store_weather_readings(raw_weather_rows)

    def parse_period(self, target_period):
        """Schedules file parsing by locating files that match requested period."""
        all_weather_readings = []
        file_pattern = WeatherParserUtility.generate_file_pattern(target_period)

        if not file_pattern:
           
            return []

        matching_files = list(self.directory_path.glob(file_pattern))

        if not matching_files:
            print(f"No data files found matching pattern: {file_pattern}")
        else:
            for filepath in matching_files:
                all_weather_readings.extend(self._parse_file(filepath))

        return all_weather_readings
