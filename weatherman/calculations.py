import data_models
import calendar
from constants import DEFAULT_VALUE


class WeatherCalculator:
    """Encapsulates weather data calculations."""

    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    @staticmethod
    def calculate_weather_readings_average(weather_reading_value):
        """function to calculate averages"""

        return (
            sum(weather_reading_value) / len(weather_reading_value)
            if weather_reading_value
            else DEFAULT_VALUE
        )

    @staticmethod
    def _handle_missing_values(weather_value):
        """safely handle missing daily data values."""

        return weather_value if weather_value is not None else DEFAULT_VALUE

    def _extract_valid_attributes(self, attribute_name):
        """Extracts non-None attributes from the internal readings."""

        return [
            getattr(weather_reading, attribute_name)
            for weather_reading in self.weather_readings
            if getattr(weather_reading, attribute_name) is not None
        ]

    def calculate_average_monthly_report(self):
        """calculate the average monthly max/min temperature and mean humidity"""
        weather_attributes = [
            ("maximum_temperature", "maximum_temperature_average"),
            ("minimum_temperature", "minimum_temperature_average"),
            ("mean_humidity", "mean_humidity_average"),
        ]

        extracted_weather_attributes = {
            attribute_name: self._extract_valid_attributes(attribute_name)
            for attribute_name, _ in weather_attributes
        }

        return data_models.AverageResults(
            self.calculate_weather_readings_average(
                extracted_weather_attributes["maximum_temperature"]
            ),
            self.calculate_weather_readings_average(
                extracted_weather_attributes["minimum_temperature"]
            ),
            self.calculate_weather_readings_average(
                extracted_weather_attributes["mean_humidity"]
            ),
        )

    def calculate_monthly_report(self):
        """gets the monthly min and max temperature data"""
        highest_temps = []
        lowest_temps = []

        year_str = ""
        month_name = "N/A"

        for weather_reading in self.weather_readings:
            highest_temps.append(
                self._handle_missing_values(weather_reading.maximum_temperature)
            )
            lowest_temps.append(
                self._handle_missing_values(weather_reading.minimum_temperature)
            )
        if weather_reading.date and not year_str:
            year_str = str(weather_reading.date.year)
            month_name = calendar.month_name[weather_reading.date.month]
        return month_name, year_str, highest_temps, lowest_temps

    def _build_daily_temperatures(self):
        """Build DailyTemperature DTOs, skipping invalid readings."""
        daily_temps = []
        for weather_reading in self.weather_readings:
            if not weather_reading:
                continue

            day_int = weather_reading.date.day
            max_temp = self._handle_missing_values(
                getattr(weather_reading, "maximum_temperature", None)
            )
            min_temp = self._handle_missing_values(
                getattr(weather_reading, "minimum_temperature", None)
            )

            daily_temps.append(
                data_models.DailyTemperature(day_int, max_temp, min_temp)
            )

        return daily_temps

    def calculate_chart_data(self):
        """Parses data into a ChartResults object for bonus mixed charts."""
        daily_temps = self._build_daily_temperatures()

        year_str, month_name = "", "Unknown"
        for reading in self.weather_readings:
            if reading.date:
                year_str = str(reading.date.year)
                month_name = calendar.month_name[reading.date.month]

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
        result_extreme = current_extreme_value
        result_date = current_record_date

        if new_extreme_value is not None:
            is_new_record = current_extreme_value is None or (
                (new_extreme_value > current_extreme_value)
                if find_max
                else (new_extreme_value < current_extreme_value)
            )
            if is_new_record:
                result_extreme = new_extreme_value
                result_date = new_extreme_date

        return result_extreme, result_date

    def _find_extreme_for_attribute(self, attribute_name, find_max=True):
        """Iterates through readings to find the extreme of a single attribute."""
        extreme_val, extreme_date = None, None

        for reading in self.weather_readings:
            extreme_val, extreme_date = self._evaluate_extreme(
                extreme_val,
                extreme_date,
                getattr(reading, attribute_name, None),
                reading.date,
                find_max,
            )

        return extreme_val, extreme_date

    def calculate_extreme_values(self):
        """Gets the max temperature, min temperature and max humidity with their dates"""
        highest_temp, highest_date = self._find_extreme_for_attribute(
            "maximum_temperature", find_max=True
        )
        lowest_temp, lowest_date = self._find_extreme_for_attribute(
            "minimum_temperature", find_max=False
        )
        max_humidity, humidity_date = self._find_extreme_for_attribute(
            "maximum_humidity", find_max=True
        )

        return data_models.ExtremeResults(
            maximum_temperature=highest_temp,
            maximum_temperature_date=highest_date,
            minimum_temperature=lowest_temp,
            minimum_temperature_date=lowest_date,
            maximum_humidity=max_humidity,
            maximum_humidity_date=humidity_date,
        )
