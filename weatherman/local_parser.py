import os
import csv
import glob
import calendar
import data_models
from datetime import date
from constants import (
    COLUMN_KEY_DATE,
    COLUMN_KEY_MAX_TEMP,
    COLUMN_KEY_MIN_TEMP,
    COLUMN_KEY_MAX_HUMIDITY,
    COLUMN_KEY_MEAN_HUMIDITY,
    DATE_YEAR_INDEX,
    DATE_MONTH_INDEX,
    DATE_DAY_INDEX
)


def safe_float(raw_value):
    """Converts a string to a float, safely returning None for missing or invalid data."""
    if raw_value and str(raw_value).strip() not in ("", "None"):        
        return float(str(raw_value).strip())
    return None

def safe_date(date_str):
    """SRP Helper: Exclusively parses and validates dates at the boundaries."""
    if not date_str:
        return None
    try:
        parts = date_str.replace("/", "-").split("-")
        return date(
            int(parts[DATE_YEAR_INDEX]), 
            int(parts[DATE_MONTH_INDEX]), 
            int(parts[DATE_DAY_INDEX])
        )
    except (ValueError, IndexError):
        return None
    

def _extract_raw_rows(filepath):
    """Handles File I/O: Reads a CSV file using DictReader and returns the valid raw rows."""
    raw_rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                if row.get(COLUMN_KEY_DATE) and row.get(COLUMN_KEY_DATE).strip():
                    raw_rows.append(row)

    except OSError as error:
        print(f"Error reading file: {filepath}\nException: {error}")

    return raw_rows


def _build_weather_readings(raw_rows):
    """Handles Data Modeling: Converts raw CSV dict rows into WeatherReading objects."""
    parsed_readings = []

    for row in raw_rows:
        date_value = safe_date(row.get(COLUMN_KEY_DATE, "").strip())

        if date_value:
            weather_reading = data_models.WeatherReading(
                date = date_value,
                maximum_temperature=safe_float(row.get(COLUMN_KEY_MAX_TEMP)),
                minimum_temperature=safe_float(row.get(COLUMN_KEY_MIN_TEMP)),
                maximum_humidity=safe_float(row.get(COLUMN_KEY_MAX_HUMIDITY)),
                mean_humidity=safe_float(row.get(COLUMN_KEY_MEAN_HUMIDITY))
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
        file_pattern = os.path.join(
            directory_path, f"Murree_weather_{target_year}_*.txt"
        )
    else:
        try:
            month_num = int(date_parts[DATE_MONTH_INDEX])
            month_abbr = calendar.month_abbr[month_num]
            file_pattern = os.path.join(
                directory_path, 
                f"Murree_weather_{target_year}_{month_abbr}.txt"
            )
        except (ValueError, IndexError):
            file_pattern = os.path.join(
                directory_path, f"Murree_weather_{target_year}_*.txt"
            )

    return file_pattern


def parse_manager(target_period, directory_path):
    """Schedules file parsing by locating files that match the requested period."""
    all_weather_readings = []

    file_pattern = _generate_file_pattern(
        target_period, 
        directory_path
    )
    matching_files = glob.glob(file_pattern)

    if not matching_files:
        print(f"No data files found matching pattern: {file_pattern}")
    else:
        for filepath in matching_files:
            all_weather_readings.extend(file_parse(filepath))

    return all_weather_readings