import csv

# import pandas as pd

# to parse:
# min/max temps
# max humidity + avg humidity

"try using pandas to parse the data and calculate the required values"


def single_file_parse(filename):
    try:
        FIELDS_TO_READ = [1, 3, 7, 9]
        fields = []
        rows = []

        with open(
            "C:\\Softwares\\Cogent Training\\weatherman\\weatherfiles\\" + filename, "r"
        ) as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                if len(row) <= max(FIELDS_TO_READ):
                    continue

                picked = [row[i] for i in FIELDS_TO_READ]
                rows.append(picked)
            print("File parsed:", filename)

        fields = [fields[i] for i in FIELDS_TO_READ]
        # print(
        #     "filed 1 :", fields[1],
        #     "filed 3 :", fields[3],
        #     "filed 7 :", fields[7],
        #     "filed 9 :", fields[9]
        # )
        print("fields:", fields)
        print("readings_data:", rows)

    except FileNotFoundError:
        print("File not found:", filename)

    return rows


def parsemanager(period):
    year, month = (period.split("/") + [None, None])[:2]
    print("Year:", year, "Month:", month)

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    data = []

    if month is None:
        print("Parse all files of:", year)
        for month in months:
            filename = "Murree_weather_" + year + "_" + month + ".txt"
            print("Parsing file:", filename)
            data = single_file_parse(filename)

    else:  # parse file of the given month
        # month number to month name mapping
        month = months[int(month) - 1]
        filename = "Murree_weather_" + year + "_" + month + ".txt"
        print("Parse file of ", month, " , ", year)
        print("Parsing single file:", filename)
        data = single_file_parse(filename)

    return data
