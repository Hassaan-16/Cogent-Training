from local_parser import parse_manager
from argparse import ArgumentParser
from reports import report_manager


def main():
    parser = ArgumentParser(description="weatherman CLI weather analyser")
    parser.add_argument("filepath", help="path to the file directory")
    parser.add_argument("-c", dest="chart_month", help="year/month chart values report")
    report_configs = [
        ("-e", "extreme_year", "Year for extreme values report"),
        ("-a", "average_month", "year/month for average values report"),
        ("-c", "chart_month", "year/month chart values report"),
        ("-b", "bonus_month", "Year/Month for the bonus chart"),
    ]
    for flag, dest_name, help_text in report_configs:
        parser.add_argument(flag, dest=dest_name, help=help_text)

    arguments = parser.parse_args()

    for flag, dest_name, _ in report_configs:
        target_period = getattr(arguments, dest_name)

        if target_period:
            parsed_data = parse_manager(target_period, arguments.filepath)
            report_manager(flag, parsed_data)


if __name__ == "__main__":
    main()
