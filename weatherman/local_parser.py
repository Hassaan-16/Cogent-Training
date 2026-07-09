import data_models
import constants
import calendar
import csv
import os


def safe_float(value):
    """Convert a string to a float, returning None if invalid or empty."""
    value = str(value).strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def file_parse(filepath):
    """Parse a weather CSV file and return a list of WeatherReading objects given the file path"""
    try:
        COLUMNS_TO_READ = constants.COLUMNS_TO_READ
        rows = []

        with open(filepath, "r", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)

            for row in csvreader:
                if len(row) <= max(COLUMNS_TO_READ):
                    continue

                date_str = row[0]
                max_t = safe_float(row[1])
                min_t = safe_float(row[3])
                max_h = safe_float(row[7])
                min_h = safe_float(row[9])

                weather_reading = data_models.WeatherReading(
                    date_str, max_t, min_t, max_h, min_h
                )
                rows.append(weather_reading)

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading file: {filepath}")
        print(f"Exception: {e}")

    return rows


def parse_manager(period, path):
    """schedules file_parse based on the period given by user (month/year)"""
    parts = period.split("/")
    year = parts[0]
    month = parts[1] if len(parts) > 1 else None

    months = [calendar.month_abbr[i] for i in range(1, 13)]
    data = []

    if month is None:
        for month in months:  # parse all files since month is not given
            filename = constants.FILE_NAME_FORMAT.format(year=year, month=month)
            filepath = os.path.join(path, filename)
            data.extend(file_parse(filepath))

    else:
        month = months[int(month) - 1]
        filename = constants.FILE_NAME_FORMAT.format(year=year, month=month)
        print("Parsing file:", filename)
        filepath = os.path.join(path, filename)
        data = file_parse(filepath)

    return data
