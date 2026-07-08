import sys
import re       #
import fnmatch  #
import csv
import parser

def main():
    print("Arguments passed:", sys.argv)
    # 0: script name
    # 1: filepath
    # 2: mode (-a, -c, -e)
    # 3: year/month 

    parser.parsemanager(sys.argv[3])

    # loop through the args=3 step 2 (for year/month)

if __name__ == "__main__":
    main()