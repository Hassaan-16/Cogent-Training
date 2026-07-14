from argparse import ArgumentParser
from local_parser import WeatherParser
from calculations import WeatherCalculator
from reports import ReportGenerator


def main():
    parser = ArgumentParser(description="weatherman CLI weather analyser")
    parser.add_argument("filepath", help="path to the file directory")

    report_configs = [
        ("-e", "extreme_year", "Year for extreme values report"),
        ("-a", "average_month", "year/month for average values report"),
        ("-c", "chart_month", "year/month chart values report"),
        ("-b", "bonus_month", "Year/Month for the bonus chart"),
    ]

    for command_line_flag, report_type, help_text in report_configs:
        parser.add_argument(command_line_flag, dest=report_type, help=help_text)

    command_line_arguments = parser.parse_args()

    parser_service = WeatherParser(command_line_arguments.filepath)

    for command_line_flag, report_type, _ in report_configs:
        target_period = getattr(command_line_arguments, report_type)

        if target_period:
            parsed_readings = parser_service.parse_period(target_period)

            if parsed_readings:
                calculator = WeatherCalculator(parsed_readings)
                report_service = ReportGenerator(calculator)

                report_service.execute_report(command_line_flag)


if __name__ == "__main__":
    main()
