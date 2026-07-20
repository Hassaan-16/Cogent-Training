import calendar

from constants import (
    MINIMUM_VALUE,
    RESET_ASCII,
    RED_ASCII,
    BLUE_ASCII,
    DATE_MONTH_INDEX,
    DATE_DAY_INDEX,
    LABEL_HIGHEST,
    LABEL_LOWEST,
    LABEL_HUMIDITY,
    UNIT_CELSIUS,
    UNIT_PERCENT,
)


def format_temp_int(temperature_in_degrees):
    """temperature rounding as integers. None values returned as N/A."""
    if temperature_in_degrees is None:
        return "N/A"

    return int(round(temperature_in_degrees))


def format_extreme_value(extreme_weather_reading, date_object, unit="C"):
    """Formats an extreme value with weather reading and unit. returns 'N/A' if None"""
    if None not in [extreme_weather_reading, date_object]:
        month_name = calendar.month_name[date_object.month]
        date_str = f"{month_name} {date_object.day:02d}"

        formatted_temp = format_temp_int(extreme_weather_reading)
        formatted_extreme_value_str = f"{formatted_temp}{unit} on {date_str}"

    else:
        formatted_extreme_value_str = "N/A"

    return formatted_extreme_value_str


def build_color_bar(temperature_in_degrees, ascii_color_code):
    """Builds a single colored ASCII bar based on ASCII code."""
    temperature_in_degrees = max(temperature_in_degrees, MINIMUM_VALUE)

    return f"{ascii_color_code}{'+' * temperature_in_degrees}{RESET_ASCII}"


def build_combined_color_bar(min_temp_int, max_temp_int):
    """Calculates and concatenates the dual-color ASCII bar."""
    blue_bar = build_color_bar(min_temp_int, BLUE_ASCII)
    red_bar = build_color_bar(max_temp_int - min_temp_int, RED_ASCII)

    return blue_bar.replace(RESET_ASCII, "") + red_bar


def format_bonus_chart_row(day_num, combined_bar, min_temp, max_temp):
    """Handles the strict string layout for a single bonus chart row."""

    return f"{day_num:02d} {combined_bar} {min_temp}C-{max_temp}C"


def format_chart_row(day_num, bar, temp):
    """Returns formatted string lines for the monthly chart report."""

    return f"{day_num:02d} {bar} {temp}C"


def format_monthly_chart_lines(month_name, year_str, highest_temps, lowest_temps):
    """Creates formatted string lines for the monthly chart report."""
    lines = [f"{month_name} {year_str}"]

    for day_index, (high, low) in enumerate(zip(highest_temps, lowest_temps), start=1):
        if high is None or low is None:
            continue

        formatted_high = format_temp_int(high)
        formatted_low = format_temp_int(low)

        lines.append(
            format_chart_row(
                day_index, build_color_bar(formatted_high, RED_ASCII), high
            )
        )
        lines.append(
            format_chart_row(day_index, build_color_bar(formatted_low, BLUE_ASCII), low)
        )

    return lines


def get_bonus_chart_lines(daily_temps):
    """Creates formatted string lines for the combined bonus chart."""
    if not daily_temps.dailyTemperature:
        return ["No daily temperatures found to chart."]

    bonus_chart_lines = [f"{daily_temps.month_name} {daily_temps.year}"]

    for daily in daily_temps.dailyTemperature:
        if daily.maximum_temperature is None or daily.minimum_temperature is None:
            continue

        day_num = daily.day
        min_temp = format_temp_int(daily.minimum_temperature)
        max_temp = format_temp_int(daily.maximum_temperature)

        combined_bar = build_combined_color_bar(min_temp, max_temp)

        formatted_row = format_bonus_chart_row(
            day_num, combined_bar, min_temp, max_temp
        )

        bonus_chart_lines.append(formatted_row)

    return bonus_chart_lines


def get_average_monthly_lines(average_metrics):
    """Builds formatted string lines for the average monthly report."""
    high_temp_avg = format_temp_int(average_metrics.average_maximum_temperature)
    low_temp_avg = format_temp_int(average_metrics.average_minimum_temperature)
    humidity_avg = format_temp_int(average_metrics.average_humidity)

    average_monthly_lines = [
        f"Highest Average: {high_temp_avg}C",
        f"Lowest Average: {low_temp_avg}C",
        f"Average Mean Humidity: {humidity_avg}%",
    ]

    return average_monthly_lines


def get_extreme_values_lines(extreme_metrics):
    """Builds formatted string lines for the extreme values report using constants."""
    report_configs = [
        (
            LABEL_HIGHEST,
            extreme_metrics.maximum_temperature,
            extreme_metrics.maximum_temperature_date,
            UNIT_CELSIUS,
        ),
        (
            LABEL_LOWEST,
            extreme_metrics.minimum_temperature,
            extreme_metrics.minimum_temperature_date,
            UNIT_CELSIUS,
        ),
        (
            LABEL_HUMIDITY,
            extreme_metrics.maximum_humidity,
            extreme_metrics.maximum_humidity_date,
            UNIT_PERCENT,
        ),
    ]

    extreme_values = [
        f"{extreme_value_label}: {format_extreme_value(extreme_value, date_obj, unit)}"
        for extreme_value_label, extreme_value, date_obj, unit in report_configs
    ]

    return extreme_values
