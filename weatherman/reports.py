import calendar
from constants import (
    MINIMUM_VALUE,
    RESET_ASCII,
    RED_ASCII,
    BLUE_ASCII,
)


class ReportGenerator:
    """Handles printing and formatting of weather reports."""

    def __init__(self, calculator):
        self.calculator = calculator

    @staticmethod
    def _format_temp_int(temperature_in_degrees):
        """Standardizes temperature rounding and formatting as integers"""

        return int(round(temperature_in_degrees))

    @staticmethod
    def _build_color_bar(temperature_in_degrees, ascii_color_code):
        """Builds a single colored ASCII bar based on ASCII code"""
        if temperature_in_degrees < MINIMUM_VALUE:
            temperature_in_degrees = MINIMUM_VALUE

        return f"{ascii_color_code}{'+' * temperature_in_degrees}{RESET_ASCII}"

    @staticmethod
    def _format_extreme_value(self, extreme_weather_reading, date_object, unit="C"):
        """Formats an extreme value string safely handling None and extracting clean date strings."""
        if extreme_weather_reading is not None and date_object is not None:
            month_name = calendar.month_name[date_object.month]
            date_str = f"{month_name} {date_object.day:02d}"
            formatted_temp = self._format_temp_int(extreme_weather_reading)
            formatted_extreme_value_str = f"{formatted_temp}{unit} on {date_str}"
        else:
            formatted_extreme_value_str = "N/A"

        return formatted_extreme_value_str

    def generate_average_monthly_report(self):
        """Generates the average monthly report from an AverageResults object."""
        average_metrics = self.calculator.calculate_average_monthly_report()

        print(
            f"Highest Average: {
                self._format_temp_int(average_metrics.average_maximum_temperature)
            }C"
        )
        print(
            f"Lowest Average: {
                self._format_temp_int(average_metrics.average_minimum_temperature)
            }C"
        )
        print(
            f"Average Mean Humidity: {
                self._format_temp_int(average_metrics.average_humidity)
            }%"
        )

    def generate_monthly_charts(self):
        """Generates console horizontal bar charts for monthly data."""
        month_name, year_str, highest_temp, lowest_temp = (
            self.calculator.calculate_monthly_report()
        )

        print(f"{month_name} {year_str}")

        for day_index in range(len(highest_temp)):
            day_high_temperature = highest_temp[day_index]
            day_low_temperature = lowest_temp[day_index]

            if (
                day_high_temperature == MINIMUM_VALUE
                and day_low_temperature == MINIMUM_VALUE
            ):
                continue

            formatted_high = self._format_temp_int(day_high_temperature)
            formatted_low = self._format_temp_int(day_low_temperature)

            high_temperature_bar = self._build_color_bar(formatted_high, RED_ASCII)
            low_temperature_bar = self._build_color_bar(formatted_low, BLUE_ASCII)

            print(f"{day_index + 1:02d} {high_temperature_bar} {day_high_temperature}C")
            print(f"{day_index + 1:02d} {low_temperature_bar} {day_low_temperature}C")

    def generate_bonus_charts(self):
        """Generates one combined chart for highest and lowest temperatures each day"""
        daily_temps = self.calculator.calculate_chart_data()

        if not daily_temps.dailyTemperature:
            print("No daily temperatures found to chart.")

            return

        print(f"{daily_temps.month_name} {daily_temps.year}")

        for daily_temperatures in daily_temps.dailyTemperature:
            if (
                daily_temperatures.maximum_temperature == MINIMUM_VALUE
                and daily_temperatures.minimum_temperature == MINIMUM_VALUE
            ):
                continue

            day_number = daily_temperatures.day
            min_temperature = self._format_temp_int(
                daily_temperatures.minimum_temperature
            )
            max_temperature = self._format_temp_int(
                daily_temperatures.maximum_temperature
            )

            safe_min_temp = max(MINIMUM_VALUE, min_temperature)
            safe_max_temp = max(MINIMUM_VALUE, max_temperature)

            blue_bar = self._build_color_bar(safe_min_temp, BLUE_ASCII)
            red_bar = self._build_color_bar(safe_max_temp - safe_min_temp, RED_ASCII)

            combined_bar = blue_bar.replace(RESET_ASCII, "") + red_bar

            print(
                f"{day_number:02d} {combined_bar} {min_temperature}C-{max_temperature}C"
            )

    def generate_extreme_values_report(self):
        """generate the extreme values report (year)"""
        extreme_metrics = self.calculator.calculate_extreme_values()

        report_configs = [
            (
                "Highest",
                extreme_metrics.maximum_temperature,
                extreme_metrics.maximum_temperature_date,
                "C",
            ),
            (
                "Lowest",
                extreme_metrics.minimum_temperature,
                extreme_metrics.minimum_temperature_date,
                "C",
            ),
            (
                "Humidity",
                extreme_metrics.maximum_humidity,
                extreme_metrics.maximum_humidity_date,
                "%",
            ),
        ]

        report_dict = {
            extreme_value_label: self._format_extreme_value(
                metric_value, metric_date, unit
            )
            for extreme_value_label, metric_value, metric_date, unit in report_configs
        }

        for extreme_value_label, extreme_value in report_dict.items():
            print(f"{extreme_value_label}: {extreme_value}")

    def execute_report(self, report_type):
        """Selects and executes the appropriate report generation based on the mode."""
        dispatch = {
            "-a": self.generate_average_monthly_report,
            "-c": self.generate_monthly_charts,
            "-b": self.generate_bonus_charts,
            "-e": self.generate_extreme_values_report,
        }

        if report_type in dispatch:
            dispatch[report_type]()
            print(" ")
        else:
            print("Invalid mode. Please use -a, -c, -e, or -b.")
