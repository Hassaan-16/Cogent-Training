from calculations import (
    calculate_average_monthly_report,
    calculate_chart_data,
    calculate_extreme_values,
    calculate_monthly_report,
)
from constants import (
    MINIMUM_VALUE,
    RESET_ASCII,
    RED_ASCII,
    BLUE_ASCII,
)
import calendar


def format_extreme_value(extreme_value, date_object, unit="C"):
    """DRY Helper: Formats an extreme value string safely handling None and extracting clean date strings."""
    if extreme_value is not None and date_object is not None:
        month_name = calendar.month_name[date_object.month]
        date_str = f"{month_name} {date_object.day:02d}"
    
        return f"{int(round(extreme_value))}{unit} on {date_str}"
    
    return "N/A"


def generate_average_monthly_report(average_metrics):
    """Generates the average monthly report from an AverageResults object."""
    print(f"Highest Average: {int(round(average_metrics.average_maximum_temperature))}C")
    print(f"Lowest Average: {int(round(average_metrics.average_minimum_temperature))}C")
    print(f"Average Mean Humidity: {int(round(average_metrics.average_humidity))}%")


def generate_monthly_charts(highest_temp, lowest_temp):
    """Generates console horizontal bar charts for monthly data."""
    for day_index in range(len(highest_temp)):
        day_high_temperature = highest_temp[day_index]
        day_low_temperature = lowest_temp[day_index]

        if (
            day_high_temperature == MINIMUM_VALUE
            and day_low_temperature == MINIMUM_VALUE
        ):
            continue

        high_temperature_bar = (
            RED_ASCII 
            + ("+" * int(round(day_high_temperature))) 
            + RESET_ASCII
        )
        low_temperature_bar = (
            BLUE_ASCII 
            + ("+" * int(round(day_low_temperature))) 
            + RESET_ASCII
        )

        print(f"{day_index+1:02d} {high_temperature_bar} {day_high_temperature}C")
        print(f"{day_index+1:02d} {low_temperature_bar} {day_low_temperature}C")


def generate_bonus_charts(daily_temps):
    """Generates one combined chart for highest and lowest temperatures each day"""
    if not daily_temps.dailyTemperature:
        print("No daily temperatures found to chart.")
        
        return

    print(f"{daily_temps.month_name} {daily_temps.year}")

    for daily_temperatures in daily_temps.dailyTemperature:
        if (
            daily_temperatures.maximum_temperature == MINIMUM_VALUE
            and daily_temperatures.minimum_temperature == MINIMUM_VALUE
        ):
            continue

        day_number = daily_temperatures.day
        min_temperature = int(round(daily_temperatures.minimum_temperature))
        max_temperature = int(round(daily_temperatures.maximum_temperature))

        blue_pluses = "+" * max(MINIMUM_VALUE, min_temperature)
        red_pluses = "+" * max(MINIMUM_VALUE, (max_temperature - min_temperature))

        combined_bar = BLUE_ASCII + blue_pluses + RED_ASCII + red_pluses + RESET_ASCII

        print(f"{day_number:02d} {combined_bar} {min_temperature}C-{max_temperature}C")


def generate_extreme_values_report(extreme_metrics):
    """generate the extreme values report (year)"""
    highest_str = format_extreme_value(
        extreme_metrics.maximum_temperature,
        extreme_metrics.maximum_temperature_date,
        "C",
    )
    lowest_str = format_extreme_value(
        extreme_metrics.minimum_temperature,
        extreme_metrics.minimum_temperature_date,
        "C",
    )
    humidity_str = format_extreme_value(
        extreme_metrics.maximum_humidity,
        extreme_metrics.maximum_humidity_date,
        "%",
    )

    return {
        "Highest": highest_str,
        "Lowest": lowest_str,
        "Humidity": humidity_str,
    }


def print_extreme_values_report(report_dict):
    for label, text in report_dict.items():
        print(f"{label}: {text}")


def report_manager(report_type, parsed_readings):
    """Selects and executes the appropriate report generation based on the mode."""
    dispatch = {
        "-a": lambda weather_readings: 
        generate_average_monthly_report(
            calculate_average_monthly_report(weather_readings)
            ),
        "-c": lambda weather_readings: 
        generate_monthly_charts(
            *calculate_monthly_report(weather_readings)
            ),
        "-b": lambda weather_readings: 
        generate_bonus_charts(
            calculate_chart_data(weather_readings)
            ),
        "-e": lambda weather_readings: 
        print_extreme_values_report(
            generate_extreme_values_report(
                calculate_extreme_values(weather_readings)),
            )
    }

    if report_type in dispatch:
        dispatch[report_type](parsed_readings)
    else:
        print("Invalid mode. Please use -a, -c, -e, or -b.")