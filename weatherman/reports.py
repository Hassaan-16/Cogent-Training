from formatters import FormatterHelper
from constants import FLAG_AVERAGE, FLAG_BONUS, FLAG_CHART, FLAG_EXTREME


class ReportGenerator:
    """Handles printing and formatting of the weather reports."""

    def __init__(self, calculator):
        self.calculator = calculator

    def generate_average_monthly_report(self):
        """Generates the average monthly report"""
        average_metrics = self.calculator.calculate_average_monthly_report()

        return FormatterHelper.get_average_monthly_lines(average_metrics)

    def generate_monthly_charts(self):
        """Generates the horizontal bar charts for monthly data."""
        month_name, year_str, highest_temp, lowest_temp = (
            self.calculator.build_monthly_report()
        )

        return FormatterHelper.get_monthly_chart_lines(
            month_name, year_str, highest_temp, lowest_temp
        )

    def generate_bonus_charts(self):
        """Generates one combined daily chart."""
        daily_temps = self.calculator.calculate_chart_data()

        return FormatterHelper.get_bonus_chart_lines(daily_temps)

    def generate_extreme_values_report(self):
        """Generates the extreme values report."""
        extreme_metrics = self.calculator.calculate_extreme_values()

        return FormatterHelper.get_extreme_values_lines(extreme_metrics)

    def _print_report_lines(self, formatted_report_lines):
        """Displays formatted lines for any generated report."""
        for formatted_line in formatted_report_lines:
            print(formatted_line)

    def execute_report(self, report_type):
        """Selects and executes the appropriate report generation based on the mode."""
        dispatch = {
            FLAG_AVERAGE: self.generate_average_monthly_report,
            FLAG_BONUS: self.generate_bonus_charts,
            FLAG_CHART: self.generate_monthly_charts,
            FLAG_EXTREME: self.generate_extreme_values_report,
        }

        if report_type in dispatch:
            formatted_lines = dispatch[report_type]()
            self._print_report_lines(formatted_lines)
            print("")    
