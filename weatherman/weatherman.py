import sys
import csv
import local_parser
import reports

def main():
    print("Arguments passed:", sys.argv)
    # 0: script name
    # 1: filepath
    # 2: mode (-a, -c, -e)
    # 3: period (year/month)

    # loop through the args=3 step 2 (for year/month) for cols 2,4,8,10

    mode = sys.argv[2]
    period = sys.argv[3]
    parsed_data = local_parser.parsemanager(period)
    # process the parsed data based on the mode
    reports.report_manager(mode,parsed_data)

if __name__ == "__main__":
    main()