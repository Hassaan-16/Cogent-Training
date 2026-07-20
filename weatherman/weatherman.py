from argparse import ArgumentParser

from calculations import WeatherCalculator
from constants import (
    ARG_FILEPATH,
    CLI_DESCRIPTION,
    DEST_AVERAGE,
    DEST_BONUS,
    DEST_CHART,
    DEST_EXTREME,
    FLAG_AVERAGE,
    FLAG_BONUS,
    FLAG_CHART,
    FLAG_EXTREME,
    HELP_AVERAGE,
    HELP_BONUS,
    HELP_CHART,
    HELP_EXTREME,
    HELP_FILEPATH,
)
from reports import ReportGenerator
from weather_parser import WeatherParser


def main():
    parser = ArgumentParser(description=CLI_DESCRIPTION)

    parser.add_argument(ARG_FILEPATH, help=HELP_FILEPATH)

    report_configs = [
        (FLAG_AVERAGE, DEST_AVERAGE, HELP_AVERAGE),
        (FLAG_BONUS, DEST_BONUS, HELP_BONUS),
        (FLAG_CHART, DEST_CHART, HELP_CHART),
        (FLAG_EXTREME, DEST_EXTREME, HELP_EXTREME),
    ]

    # Re-added the loop to register the arguments
    for command_line_flag, report_type, help_text in report_configs:
        parser.add_argument(
            command_line_flag, dest=report_type, help=help_text, action="append"
        )

    command_line_arguments = parser.parse_args()
    parser_service = WeatherParser(command_line_arguments.filepath)

    for command_line_flag, report_type, _ in report_configs:
        target_periods = getattr(command_line_arguments, report_type)

        if not target_periods:
            continue

        for target_period in target_periods:
            parsed_readings = parser_service.parse_period(target_period)

            if not parsed_readings:
                continue

            calculator = WeatherCalculator(parsed_readings)
            report_service = ReportGenerator(calculator)

            report_service.execute_report(command_line_flag)


if __name__ == "__main__":
    main()
