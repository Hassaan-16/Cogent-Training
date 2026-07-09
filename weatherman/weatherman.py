import local_parser
import argparse
import reports


def main():
    parser = argparse.ArgumentParser(description="weatherman CLI weather analyser")
    parser.add_argument("filepath", help="path to the file directory")
    parser.add_argument(
        "-e", dest="extreme_year", help="Year for extreme values report"
    )
    parser.add_argument(
        "-a", dest="average_month", help="year/month for average values report"
    )
    parser.add_argument("-c", dest="chart_month", help="year/month chart values report")
    parser.add_argument(
        "-b", dest="bonus_month", help="Year/Month for Task 5 bonus chart"
    )

    args = parser.parse_args()

    if args.extreme_year:
        parsed_data = local_parser.parse_manager(args.extreme_year, args.filepath)
        reports.report_manager("-e", parsed_data)

    if args.average_month:
        parsed_data = local_parser.parse_manager(args.average_month, args.filepath)
        reports.report_manager("-a", parsed_data)

    if args.chart_month:
        parsed_data = local_parser.parse_manager(args.chart_month, args.filepath)
        reports.report_manager("-c", parsed_data)

    if args.bonus_month:
        parsed_data = local_parser.parse_manager(args.bonus_month, args.filepath)
        reports.report_manager("-b", parsed_data)


if __name__ == "__main__":
    main()
