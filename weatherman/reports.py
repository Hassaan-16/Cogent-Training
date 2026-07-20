from formatters import FormatterHelper
from constants import FLAG_AVERAGE, FLAG_BONUS, FLAG_CHART, FLAG_EXTREME


class ReportGenerator:
    """Handles printing and formatting of the weather reports."""

    def __init__(self, calculator):
        self.calculator = calculator

    def generate_average_monthly_report(self):
        """Generates and prints the average monthly report."""
        average_metrics = self.calculator.calculate_average_monthly_report()
        formatted_average_monthly_lines = FormatterHelper.get_average_monthly_lines(
            average_metrics
        )

        for average_report_values in formatted_average_monthly_lines:
            print(average_report_values)

    def generate_monthly_charts(self):
        """Displays horizontal bar charts for monthly data."""
        month_name, year_str, highest_temp, lowest_temp = (
            self.calculator.calculate_monthly_report()
        )

        formatted_monthly_chart_lines = FormatterHelper.get_monthly_chart_lines(
            month_name, year_str, highest_temp, lowest_temp
        )

        for monthly_chart_line in formatted_monthly_chart_lines:
            print(monthly_chart_line)

    def generate_bonus_charts(self):
        """Displays one combined daily chart."""
        daily_temps = self.calculator.calculate_chart_data()
        formatted_bonus_chart_lines = FormatterHelper.get_bonus_chart_lines(daily_temps)

        for bonus_chart_line in formatted_bonus_chart_lines:
            print(bonus_chart_line)

    def generate_extreme_values_report(self):
        """Generates and prints the extreme values report."""
        extreme_metrics = self.calculator.calculate_extreme_values()
        formatted_extreme_values_lines = FormatterHelper.get_extreme_values_lines(
            extreme_metrics
        )

        for extreme_values in formatted_extreme_values_lines:
            print(extreme_values)

    def execute_report(self, report_type):
        """Selects and executes the appropriate report generation based on the mode."""
        dispatch = {
            FLAG_AVERAGE: self.generate_average_monthly_report,
            FLAG_BONUS: self.generate_bonus_charts,
            FLAG_CHART: self.generate_monthly_charts,
            FLAG_EXTREME: self.generate_extreme_values_report,
        }

        if report_type in dispatch:
            dispatch[report_type]()
            print("")
        else:
            print(
                f"Invalid mode. Please use {FLAG_AVERAGE, FLAG_BONUS, FLAG_CHART} or {
                    FLAG_EXTREME
                }"
            )
