import calculations
import constants


def generate_average_monthly_report(results):
    """Generates the average monthly report from an AverageResults object."""
    print(f"Highest Average: {int(round(results.average_max_temp))}C")
    print(f"Lowest Average: {int(round(results.average_min_temp))}C")
    print(f"Average Mean Humidity: {int(round(results.average_humidity))}%")


def generate_monthly_charts(highest_temp, lowest_temp):
    """Generates console horizontal bar charts for monthly data."""
    for i in range(len(highest_temp)):
        day_high = highest_temp[i]
        day_low = lowest_temp[i]

        if day_high == 0.0 and day_low == 0.0:
            continue

        high_bar = constants.RED + ("+" * int(round(day_high))) + constants.RESET
        low_bar = constants.BLUE + ("+" * int(round(day_low))) + constants.RESET

        print(f"{i+1:02d} {high_bar} {day_high}C")
        print(f"{i+1:02d} {low_bar} {day_low}C")


def generate_bonus_charts(results):
    """Generates one combined chart for highest and lowest temperatures each day"""
    if not results.DailyTemperature:
        print("No daily temperatures found to chart.")
        return

    print(f"{results.month_name} {results.year}")

    for daily in results.DailyTemperature:
        if daily.max_temp == 0.0 and daily.min_temp == 0.0:
            continue

        day = daily.day
        min_t = int(round(daily.min_temp))
        max_t = int(round(daily.max_temp))

        blue_pluses = "+" * max(0, min_t)
        red_pluses = "+" * max(0, (max_t - min_t))

        combined_bar = (
            constants.BLUE + blue_pluses + constants.RED + red_pluses + constants.RESET
        )

        print(f"{day:02d} {combined_bar} {min_t}C-{max_t}C")


def generate_extreme_values_report(results):
    """generate the extreme values report (year)"""
    print(f"Highest: {results.max_temp}C")
    print(f"Lowest: {results.min_temp}C")
    print(f"Humidity: {results.max_humidity}%")


def report_manager(mode, data):
    """ "selects the function based on the mode"""
    if mode == "-a":
        results = calculations.calculate_average_monthly(data)
        generate_average_monthly_report(results)
    elif mode == "-c":
        highest_temps, lowest_temps = calculations.calculate_monthly_report(data)
        generate_monthly_charts(highest_temps, lowest_temps)
    elif mode == "-b":
        results = calculations.calculate_chart_data(data)
        generate_bonus_charts(results)
    elif mode == "-e":
        results = calculations.calculate_extreme_values(data)
        generate_extreme_values_report(results)
    else:
        print("Invalid mode. Please use -a, -c, or -e.")
