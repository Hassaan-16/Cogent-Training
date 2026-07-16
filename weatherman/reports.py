from formatters import (
    get_average_monthly_lines,
    get_monthly_chart_lines,
    get_bonus_chart_lines,
    get_extreme_values_lines,
)


class ReportGenerator:
    """Handles printing and formatting of the weather reports."""

    def __init__(self, calculator):
        self.calculator = calculator

    def generate_average_monthly_report(self):
        """Generates and prints the average monthly report."""
        average_metrics = self.calculator.calculate_average_monthly_report()
        formatted_lines = get_average_monthly_lines(average_metrics)

        for line in formatted_lines:
            print(line)

    def generate_monthly_charts(self):
        """Displays horizontal bar charts for monthly data."""
        month_name, year_str, highest_temp, lowest_temp = (
            self.calculator.calculate_monthly_report()
        )

        formatted_chart_lines = get_monthly_chart_lines(
            month_name, year_str, highest_temp, lowest_temp
        )

        for line in formatted_chart_lines:
            print(line)

    def generate_bonus_charts(self):
        """Displays one combined daily chart."""
        daily_temps = self.calculator.calculate_chart_data()
        formatted_chart_lines = get_bonus_chart_lines(daily_temps)

        for line in formatted_chart_lines:
            print(line)

    def generate_extreme_values_report(self):
        """Generates and prints the extreme values report."""
        extreme_metrics = self.calculator.calculate_extreme_values()
        formatted_lines = get_extreme_values_lines(extreme_metrics)

        for line in formatted_lines:
            print(line)

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
