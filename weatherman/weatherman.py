from local_parser import parse_manager
from argparse import ArgumentParser
from reports import report_manager


def main():
    parser = ArgumentParser(
        description="weatherman CLI weather analyser"
    )
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

    for command_line_flag, report_type, _ in report_configs:
        target_period = getattr(command_line_arguments, report_type)

        if target_period:
            parsed_readings = parse_manager(
                target_period, command_line_arguments.filepath
            )
            report_manager(command_line_flag, parsed_readings)


if __name__ == "__main__":
    main()
