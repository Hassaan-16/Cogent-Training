import data_models
import calendar
from constants import (
    DEFAULT_VALUE, 
    DATE_PARTS_LIMIT, 
    DATE_MONTH_INDEX, 
    DATE_YEAR_INDEX
)


def weather_readings_average(weather_reading_value):
    """Helper function for average calculations."""
    
    return sum(weather_reading_value) / len(weather_reading_value) if weather_reading_value else DEFAULT_VALUE


def safe_weather_value(weather_value):
    """Helper function to safely handle missing daily data values."""
    
    return weather_value if weather_value is not None else DEFAULT_VALUE


def _extract_valid_attributes(weather_readings, attribute_name):
    """DRY Helper: Extracts non-None attributes from a list of objects."""
    
    return [
        getattr(weather_reading, attribute_name) 
        for weather_reading in weather_readings 
        if getattr(weather_reading, attribute_name) is not None
    ]


def calculate_average_monthly_report(weather_readings):
    """calculate the average monthly max/min temperature and mean humidity"""
    metrics = [
        ("maximum_temperature", "maximum_temperature_average"),
        ("minimum_temperature", "minimum_temperature_average"),
        ("mean_humidity", "mean_humidity_average"),
    ]

    extracted_weather_attributes = {
        attribute_name: _extract_valid_attributes(
            weather_readings, 
            attribute_name
        ) for attribute_name, _ in metrics}

    return data_models.AverageResults(
        weather_readings_average(extracted_weather_attributes["maximum_temperature"]),
        weather_readings_average(extracted_weather_attributes["minimum_temperature"]),
        weather_readings_average(extracted_weather_attributes["mean_humidity"]),
    )


def calculate_monthly_report(weather_readings):
    """gets the monthly min and max temperatures"""
    highest_temps = []
    lowest_temps = []

    for weather_reading in weather_readings:
        highest_temps.append(safe_weather_value(weather_reading.maximum_temperature))
        lowest_temps.append(safe_weather_value(weather_reading.minimum_temperature))

    return highest_temps, lowest_temps


def _build_daily_temperatures(weather_readings):
    """Build DailyTemperature DTOs, skipping invalid readings."""
    daily_temps = []
    for weather_reading in weather_readings:
        if not weather_readings:
            continue

        day_int = weather_reading.date.day
        max_temp = safe_weather_value(getattr(weather_reading, "maximum_temperature", None))
        min_temp = safe_weather_value(getattr(weather_reading, "minimum_temperature", None))

        daily_temps.append(data_models.DailyTemperature(day_int, max_temp, min_temp))

    return daily_temps


def calculate_chart_data(weather_readings):
    """Parses data into a ChartResults object for bonus mixed charts."""
    daily_temps = _build_daily_temperatures(weather_readings)

    year_str, month_name = "", "Unknown"
    for reading in weather_readings:
        if reading.date:
            year_str = str(reading.date.year)
            month_name = calendar.month_name[reading.date.month]                
            break

    return data_models.ChartResults(month_name, year_str, daily_temps)


def _evaluate_extreme(current_extreme, record_date, new_metric, new_date, find_max=True):
    """DRY Helper: Compares and returns the new extreme value and its date."""
    if new_metric is None:
        return current_extreme, record_date

    if current_extreme is None:
        return new_metric, new_date

    is_new_record = (
        (new_metric > current_extreme) if find_max else (new_metric < current_extreme)
    )

    if is_new_record:
        return new_metric, new_date

    return current_extreme, record_date


def calculate_extreme_values(weather_readings):
    """Gets the max temperature, min temperature and max humidity with their dates"""
    highest_temp, highest_date = None, ""
    lowest_temp, lowest_date = None, ""
    max_humidity, humidity_date = None, ""

    for reading in weather_readings:
        highest_temp, highest_date = _evaluate_extreme(
            highest_temp, 
            highest_date, 
            reading.maximum_temperature, 
            reading.date, 
            find_max=True
        )
        lowest_temp, lowest_date = _evaluate_extreme(
            lowest_temp, 
            lowest_date, 
            reading.minimum_temperature, 
            reading.date, 
            find_max=False
        )
        max_humidity, humidity_date = _evaluate_extreme(
            max_humidity, 
            humidity_date, 
            reading.maximum_humidity, 
            reading.date, 
            find_max=True
        )

    return data_models.ExtremeResults(
        maximum_temperature=highest_temp,
        maximum_temperature_date=highest_date,
        minimum_temperature=lowest_temp,
        minimum_temperature_date=lowest_date,
        maximum_humidity=max_humidity,
        maximum_humidity_date=humidity_date,
    )