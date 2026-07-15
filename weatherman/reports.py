from formatters import (
    format_temp_int,
    format_extreme_value,
    create_monthly_chart_lines,
    create_bonus_chart_lines,
)


class ReportGenerator:
    """Handles printing and formatting of the weather reports."""

    def __init__(self, calculator):
        self.calculator = calculator

    def generate_average_monthly_report(self):
        """Generates the average monthly report from an AverageResults object."""
        average_weather_metrics = self.calculator.calculate_average_monthly_report()

        high_avg = format_temp_int(average_weather_metrics.average_maximum_temperature)
        low_avg = format_temp_int(average_weather_metrics.average_minimum_temperature)
        humidity_avg = format_temp_int(average_weather_metrics.average_humidity)

        print(f"Highest Average: {high_avg}C")
        print(f"Lowest Average: {low_avg}C")
        print(f"Average Mean Humidity: {humidity_avg}%")

    def generate_monthly_charts(self):
        """Displays horizontal bar charts for monthly data without formatting logic."""
        month_name, year_str, highest_temp, lowest_temp = (
            self.calculator.calculate_monthly_report()
        )

        formatted_chart_lines = create_monthly_chart_lines(
            month_name, year_str, highest_temp, lowest_temp
        )

        for bar_chart in formatted_chart_lines:
            print(bar_chart)

    def generate_bonus_charts(self):
        """Displays one combined chart without internal formatting logic."""
        daily_temps = self.calculator.calculate_chart_data()

        formatted_chart_lines = create_bonus_chart_lines(daily_temps)

        for bar_chart in formatted_chart_lines:
            print(bar_chart)

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
            extreme_value_label: format_extreme_value(metric_value, metric_date, unit)
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
            print("")
        else:
            print("Invalid mode. Please use -a, -c, -e, or -b.")
