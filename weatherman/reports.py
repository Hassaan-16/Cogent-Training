import calculations

def generate_average_monthly_report(data):
    # Logic to generate the average monthly report
    print("Generating average monthly report...")
    calculations.calculate_average_monthly(data)

def generate_monthly_report(data):    
    # For a given month draw two horizontal bar charts on the console for 
    # the highest and lowest temperature on each day. Highest in red and lowest in blue
    print("Generating monthly report...")
    calculations.calculate_monthly_report(data)

def generate_extreme_values_report(data):
    # Logic to generate the extreme values report (year)
    print("Generating extreme values report...")
    calculations.calculate_extreme_values(data)

def report_manager(mode,data):
    if mode == "-a":
        generate_average_monthly_report(data)
    elif mode == "-c":
        generate_monthly_report(data)
    elif mode == "-e":
        generate_extreme_values_report(data)
    else:
        print("Invalid mode. Please use -a, -c, or -e.")
