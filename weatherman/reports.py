from calculations import (
    calculate_average_monthly,
    calculate_chart_data,
    calculate_extreme_values,
    calculate_monthly_report,
)
from constants import (
    DATE_MONTH_INDEX,
    DATE_DAY_INDEX,
    MINIMUM_VALUE,
    RESET_ASCII,
    RED_ASCII,
    BLUE_ASCII,
)
import calendar


def _format_date(date_str):
    """SRP Helper: Translates YYYY-MM-DD into 'Month DD' format."""
    if not date_str:
        return ""
    try:
        parts = date_str.replace("/", "-").split("-")
        month = calendar.month_name[int(parts[DATE_MONTH_INDEX])]
        day = int(parts[DATE_DAY_INDEX])
        return f"{month} {day:02d}"
    except (ValueError, IndexError):
        return date_str


def generate_average_monthly_report(results):
    """Generates the average monthly report from an AverageResults object."""
    print(f"Highest Average: {int(round(results.average_maximum_temperature))}C")
    print(f"Lowest Average: {int(round(results.average_minimum_temperature))}C")
    print(f"Average Mean Humidity: {int(round(results.average_humidity))}%")


def generate_monthly_charts(highest_temp, lowest_temp):
    """Generates console horizontal bar charts for monthly data."""
    for record in range(len(highest_temp)):
        day_high_temperature = highest_temp[record]
        day_low_temperature = lowest_temp[record]

        if (
            day_high_temperature == MINIMUM_VALUE
            and day_low_temperature == MINIMUM_VALUE
        ):
            continue

        high_temperature_bar = (
            RED_ASCII + ("+" * int(round(day_high_temperature))) + RESET_ASCII
        )
        low_temperature_bar = (
            BLUE_ASCII + ("+" * int(round(day_low_temperature))) + RESET_ASCII
        )

        print(f"{record+1:02d} {high_temperature_bar} {day_high_temperature}C")
        print(f"{record+1:02d} {low_temperature_bar} {day_low_temperature}C")


def generate_bonus_charts(results):
    """Generates one combined chart for highest and lowest temperatures each day"""
    if not results.dailyTemperature:
        print("No daily temperatures found to chart.")
        return

    print(f"{results.month_name} {results.year}")

    for daily_temperatures in results.dailyTemperature:
        if (
            daily_temperatures.maximum_temperature == MINIMUM_VALUE
            and daily_temperatures.minimum_temperature == MINIMUM_VALUE
        ):
            continue

        day = daily_temperatures.day
        min_temp = int(round(daily_temperatures.minimum_temperature))
        max_temp = int(round(daily_temperatures.maximum_temperature))

        blue_pluses = "+" * max(MINIMUM_VALUE, min_temp)
        red_pluses = "+" * max(MINIMUM_VALUE, (max_temp - min_temp))

        combined_bar = BLUE_ASCII + blue_pluses + RED_ASCII + red_pluses + RESET_ASCII

        print(f"{day:02d} {combined_bar} {min_temp}C-{max_temp}C")


def generate_extreme_values_report(results):
    """generate the extreme values report (year)"""
    highest_date = _format_date(results.maximum_temperature_date)
    lowest_date = _format_date(results.minimum_temperature_date)
    humidity_date = _format_date(results.maximum_humidity_date)

    highest_str = (
        f"{int(round(results.maximum_temperature))}C on {highest_date}"
        if results.maximum_temperature is not None
        else "N/A"
    )
    lowest_str = (
        f"{int(round(results.minimum_temperature))}C on {lowest_date}"
        if results.minimum_temperature is not None
        else "N/A"
    )
    humidity_str = (
        f"{int(round(results.maximum_humidity))}% on {humidity_date}"
        if results.maximum_humidity is not None
        else "N/A"
    )

    print(f"Highest: {highest_str}")
    print(f"Lowest: {lowest_str}")
    print(f"Humidity: {humidity_str}")


def report_manager(mode, data):
    """Selects and executes the appropriate report generation based on the mode."""
    dispatch = {
        "-a": lambda d: generate_average_monthly_report(calculate_average_monthly(d)),
        "-c": lambda d: generate_monthly_charts(*calculate_monthly_report(d)),
        "-b": lambda d: generate_bonus_charts(calculate_chart_data(d)),
        "-e": lambda d: generate_extreme_values_report(calculate_extreme_values(d)),
    }

    if mode in dispatch:
        dispatch[mode](data)
    else:
        print("Invalid mode. Please use -a, -c, -e, or -b.")
