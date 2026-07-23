import calendar
import data_models

from constants import NOT_APPLICABLE, UNKNOWN


class ReportBuilder:
    """Encapsulates the transformation of weather readings into report metrics."""

    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    def _extract_period_identifiers(self):
        """Extracts the year and month name from the first valid reading date."""
        year_string = ""
        month_string = UNKNOWN

        if not self.weather_readings:
            return year_string, month_string

        first_valid_date = next(
            (reading.date for reading in self.weather_readings if reading.date), None
        )

        if first_valid_date:
            year_string = str(first_valid_date.year)
            month_string = calendar.month_name[first_valid_date.month]

        return year_string, month_string

    def _map_to_daily_temperatures(self):
        """Maps individual day, max and min temperatures to the daily domain model."""
        daily_temperatures_list = []

        for weather_reading in self.weather_readings:
            if (
                not weather_reading
                or weather_reading.date is None
                or weather_reading.maximum_temperature is None
                or weather_reading.minimum_temperature is None
            ):
                continue

            day_integer = weather_reading.date.day
            daily_temperatures_list.append(
                data_models.DailyTemperature(
                    day_integer,
                    weather_reading.maximum_temperature,
                    weather_reading.minimum_temperature,
                )
            )

        return daily_temperatures_list

    def build_monthly_report(self):
        """Extracts the monthly min and max temperature metrics along with the month."""
        highest_temperatures = []
        lowest_temperatures = []

        for weather_reading in self.weather_readings:
            highest_temperatures.append(weather_reading.maximum_temperature)
            lowest_temperatures.append(weather_reading.minimum_temperature)

        year_string, month_string = self._extract_period_identifiers()

        if month_string == UNKNOWN:
            month_string = NOT_APPLICABLE

        return month_string, year_string, highest_temperatures, lowest_temperatures

    def build_chart_measurements(self):
        """Parses measurements into a ChartResults object for bonus mixed charts."""
        daily_temperatures_list = self._map_to_daily_temperatures()
        year_string, month_string = self._extract_period_identifiers()

        return data_models.ChartResults(
            month_string, year_string, daily_temperatures_list
        )
