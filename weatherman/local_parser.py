import os
import csv
import glob
import calendar
import data_models
from constants import (
    COLUMNS_TO_READ,
    DATE_YEAR_INDEX,
    DATE_MONTH_INDEX,
    COLUMN_INDEX_DATE,
    COLUMN_INDEX_MAX_TEMP,
    COLUMN_INDEX_MIN_TEMP,
    COLUMN_INDEX_MAX_HUMIDITY,
    COLUMN_INDEX_MEAN_HUMIDITY,
)


def safe_float(raw_value):
    """Converts a string to a float, safely returning None for missing or invalid data."""
    if raw_value and str(raw_value).strip() not in ("", "None"):
        try:
            return float(str(raw_value).strip())
        except ValueError:
            pass
    return None


def _extract_raw_rows(filepath):
    """Handles File I/O: Reads a CSV file and returns the valid raw rows."""
    raw_rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)

            for row in csv_reader:
                if len(row) > max(COLUMNS_TO_READ):
                    raw_rows.append(row)

    except OSError as error:
        print(f"Error reading file: {filepath}\nException: {error}")

    return raw_rows


def _build_weather_readings(raw_rows):
    """Handles Data Modeling: Converts raw CSV rows into WeatherReading objects."""
    parsed_readings = []

    for row in raw_rows:
        date_string = row[COLUMN_INDEX_DATE]

        if date_string.strip():
            weather_reading = data_models.WeatherReading(
                date=date_string,
                maximum_temperature=safe_float(row[COLUMN_INDEX_MAX_TEMP]),
                minimum_temperature=safe_float(row[COLUMN_INDEX_MIN_TEMP]),
                maximum_humidity=safe_float(row[COLUMN_INDEX_MAX_HUMIDITY]),
                mean_humidity=safe_float(row[COLUMN_INDEX_MEAN_HUMIDITY]),
            )
            parsed_readings.append(weather_reading)

    return parsed_readings


def file_parse(filepath):
    """Coordinates parsing a single weather file into WeatherReading objects."""
    raw_rows = _extract_raw_rows(filepath)
    return _build_weather_readings(raw_rows)


def _generate_file_pattern(target_period, directory_path):
    """Generates the glob search pattern from the user's target period string."""
    date_parts = target_period.split("/")
    target_year = date_parts[DATE_YEAR_INDEX]

    if len(date_parts) <= DATE_MONTH_INDEX:
        return os.path.join(directory_path, f"Murree_weather_{target_year}_*.txt")

    try:
        month_num = int(date_parts[DATE_MONTH_INDEX])
        month_abbr = calendar.month_abbr[month_num]
        return os.path.join(
            directory_path, f"Murree_weather_{target_year}_{month_abbr}.txt"
        )
    except (ValueError, IndexError):
        return os.path.join(directory_path, f"Murree_weather_{target_year}_*.txt")


def parse_manager(target_period, directory_path):
    """Schedules file parsing by locating files that match the requested period."""
    aggregated_data = []

    pattern = _generate_file_pattern(target_period, directory_path)
    matching_files = glob.glob(pattern)

    if not matching_files:
        print(f"No data files found matching pattern: {pattern}")
        return aggregated_data

    for filepath in matching_files:
        aggregated_data.extend(file_parse(filepath))

    return aggregated_data
