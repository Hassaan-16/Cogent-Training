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
from file_pattern_generator import generate_file_pattern
from reading_sanitizer import ReadingSanitizer


class WeatherParser:
    """Handles discovery and parsing of weather CSV files."""

    def __init__(self, directory_path):
        self.directory_path = Path(directory_path)

    def _extract_raw_dictionaries(self, filename):
        """Reads a CSV file using DictReader and returns the raw dictionaries."""
        raw_weather_dictionaries = []
        file_path_object = Path(filename)

        try:
            with file_path_object.open("r", encoding="utf-8") as weather_file:
                weather_file_readings = csv.DictReader(weather_file)

                for file_reading_dictionary in weather_file_readings:
                    raw_weather_dictionaries.append(file_reading_dictionary)

        except OSError as error:
            print(f"Error reading file: {filename}\nException: {error}")

        return raw_weather_dictionaries

    def store_weather_readings(self, raw_weather_dictionaries):
        """Converts raw CSV dictionaries into cleanly validated WeatherReading objects."""
        parsed_readings = []

        for weather_dictionary in raw_weather_dictionaries:
            raw_date_string = weather_dictionary.get(COLUMN_KEY_DATE)

            if not raw_date_string or not raw_date_string.strip():
                continue

            parsed_date_object = ReadingSanitizer.validate_date(raw_date_string.strip())

            if parsed_date_object:
                weather_reading = data_models.WeatherReading(
                    date=parsed_date_object,
                    maximum_temperature=ReadingSanitizer.convert_to_float(
                        weather_dictionary.get(COLUMN_KEY_MAX_TEMP)
                    ),
                    minimum_temperature=ReadingSanitizer.convert_to_float(
                        weather_dictionary.get(COLUMN_KEY_MIN_TEMP)
                    ),
                    maximum_humidity=ReadingSanitizer.convert_to_float(
                        weather_dictionary.get(COLUMN_KEY_MAX_HUMIDITY)
                    ),
                    mean_humidity=ReadingSanitizer.convert_to_float(
                        weather_dictionary.get(COLUMN_KEY_MEAN_HUMIDITY)
                    ),
                )
                parsed_readings.append(weather_reading)

        return parsed_readings

    def _parse_file(self, filepath):
        """Coordinates parsing a single weather file into WeatherReading objects."""
        raw_weather_dictionaries = self._extract_raw_dictionaries(filepath)

        return self.store_weather_readings(raw_weather_dictionaries)

    def _locate_matching_files(self, target_period):
        """Locates and returns a list of file paths matching the given period."""
        file_pattern = generate_file_pattern(target_period)

        if not file_pattern:
            return []

        return list(self.directory_path.glob(file_pattern))

    def parse_period(self, target_period):
        """Coordinations file parsing for a specific requested period."""
        all_weather_readings = []
        matching_files = self._locate_matching_files(target_period)

        if not matching_files:
            print(f"No data files found matching pattern: {filepath}")
        else:
            for filepath in matching_files:
                all_weather_readings.extend(self._parse_file(filepath))

        return all_weather_readings
