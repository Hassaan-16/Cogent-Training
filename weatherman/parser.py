import sys
import csv

def singlefileparse(filename):
    # parse a single file
    # print("Inside single parse")
    # check if the file exists
    try:
        rows = []
        with open("C:\\Softwares\\Cogent Training\\weatherman\\weatherfiles\\" 
                  + filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)    
            print("File parsed:", filename)                    
    except FileNotFoundError:
        print("File not found:", filename)
        return

def parsemanager(period = sys.argv[3]):    
    year, month = (period.split('/') + [None, None])[:2]
    print("Year:", year, "Month:", month)

    # parse all files depending on whether the month is provided or not
    # if len(period) < 5:
    #     # single file parse
    #     print("Single file parse")
    # elif len(period) > 5 and len(period) <= 7:
    #     # parse all files of the same year
    #     print("Parse all files of the year", sys.argv[3])    
    # else:
    #     # parse all files of the same month
    #     print("ERROR", sys.argv[3])

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']    
    
    if month is None:       # parse all files of Year
        print("Parse all files of:", year)        
        for month in months:
                filename = "Murree_weather_" + year + "_" + month + ".txt"
                print("Parsing file:", filename)
                singlefileparse(filename)

    else:                   # parse file of the given month
        # month number to month name mapping
        month = months[int(month)-1]
        filename = "Murree_weather_" + year + "_" + month + ".txt"
        print("Parse file of ", month, " , ", year)
        print("Parsing single file:", filename)
        singlefileparse(filename)
    pass

# export { singlefileparse, parsemanager }