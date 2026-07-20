import calendar

import data_models
from constants import (
    DATE_YEAR_INDEX,
    DEFAULT_VALUE,
    MAX_HUMIDITY,
    MAX_TEMP,
    MEAN_HUMIDITY,
    MIN_TEMP,
    NOT_APPLICABLE,
    UNKNOWN,
)


class WeatherCalculator:
    """Encapsulates the weather data calculations."""

    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    @staticmethod
    def calculate_weather_readings_average(weather_reading_value):
        """function to calculate averages."""

        return (
            sum(weather_reading_value) / len(weather_reading_value)
            if weather_reading_value
            else DEFAULT_VALUE
        )

    def _extract_required_attribute(self, attribute_name):
        """Extracts the required attributes from the internal readings."""

        return [
            getattr(weather_reading, attribute_name)
            for weather_reading in self.weather_readings
            if getattr(weather_reading, attribute_name) is not None
        ]

    def calculate_average_monthly_report(self):
        """calculate average monthly max/min temperature and mean humidity."""
        weather_attributes = [MAX_TEMP, MIN_TEMP, MEAN_HUMIDITY]

        extracted_weather_attributes = {
            attribute_name: self._extract_required_attribute(attribute_name)
            for attribute_name in weather_attributes
        }

        return data_models.AverageResults(
            self.calculate_weather_readings_average(
                extracted_weather_attributes[MAX_TEMP]
            ),
            self.calculate_weather_readings_average(
                extracted_weather_attributes[MIN_TEMP]
            ),
            self.calculate_weather_readings_average(
                extracted_weather_attributes[MEAN_HUMIDITY]
            ),
        )

    def calculate_monthly_report(self):
        """gets the monthly min and max temperature data"""
        highest_temps = []
        lowest_temps = []
        year_str = ""
        month_name = NOT_APPLICABLE

        for weather_report in self.weather_readings:
            highest_temps.append(weather_report.maximum_temperature)
            lowest_temps.append(weather_report.minimum_temperature)

        if self.weather_readings and self.weather_readings[DATE_YEAR_INDEX].date:
            first_valid_date = next(
                (
                    weather_reading.date
                    for weather_reading in self.weather_readings
                    if weather_reading.date
                ),
                None,
            )

            if first_valid_date:
                year_str = str(first_valid_date.year)
                month_name = calendar.month_name[first_valid_date.month]

        return month_name, year_str, highest_temps, lowest_temps

    @staticmethod
    def _map_to_daily_temperatures(weather_readings):
        """maps DailyTemperature day, max and min temperatures to data model"""
        daily_temps = []

        for weather_reading in weather_readings:
            if not weather_reading or weather_reading.date is None:
                continue

            day_int = weather_reading.date.day
            daily_temps.append(
                data_models.DailyTemperature(
                    day_int,
                    weather_reading.maximum_temperature,
                    weather_reading.minimum_temperature,
                )
            )

        return daily_temps

    def calculate_chart_data(self):
        """Parses data into a ChartResults object for bonus mixed charts."""
        daily_temps = self._map_to_daily_temperatures(self.weather_readings)

        year_str, month_name = "", UNKNOWN

        first_valid_date = next(
            (reading.date for reading in self.weather_readings if reading.date), None
        )

        if first_valid_date:
            year_str = str(first_valid_date.year)
            month_name = calendar.month_name[first_valid_date.month]

        return data_models.ChartResults(month_name, year_str, daily_temps)

    @staticmethod
    def _evaluate_extreme(
        current_extreme_value,
        current_record_date,
        new_extreme_value,
        new_extreme_date,
        find_max=True,
    ):
        """Compares and returns the new extreme value and its date."""
        if new_extreme_value is None:
            return current_extreme_value, current_record_date

        if current_extreme_value is None:
            return new_extreme_value, new_extreme_date

        current_record = (current_extreme_value, current_record_date)
        new_record = (new_extreme_value, new_extreme_date)

        extreme_function = max if find_max else min

        result_extreme, result_date = extreme_function(
            current_record, new_record, key=lambda item: item[DATE_YEAR_INDEX]
        )

        return result_extreme, result_date

    def _find_extreme_for_attribute(self, attribute_name, find_max=True):
        """Iterates through readings to find the extreme of a single attribute."""
        extreme_val, extreme_date = None, None

        for weather_reading in self.weather_readings:
            extreme_val, extreme_date = self._evaluate_extreme(
                extreme_val,
                extreme_date,
                getattr(weather_reading, attribute_name, None),
                weather_reading.date,
                find_max,
            )

        return extreme_val, extreme_date

    def calculate_extreme_values(self):
        """Gets the max temperature, min temperature and max humidity with their dates"""
        target_attributes = {MAX_TEMP: True, MIN_TEMP: False, MAX_HUMIDITY: True}

        extreme_value_attributes = {}

        for weather_attribute, find_max in target_attributes.items():
            extreme_val, extreme_date = self._find_extreme_for_attribute(
                weather_attribute, find_max
            )

            extreme_value_attributes[weather_attribute] = extreme_val
            extreme_value_attributes[f"{weather_attribute}_date"] = extreme_date

        return data_models.ExtremeResults(**extreme_value_attributes)
