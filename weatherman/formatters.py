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
    """Formats an extreme value string safely handling None and extracting clean date strings."""
    if None not in [extreme_weather_reading, date_object]:
        if isinstance(date_object, str):
            clean_date = date_object.replace("/", "-")
            parts = clean_date.split("-")
            month_num = int(parts[DATE_MONTH_INDEX])
            day_num = int(parts[DATE_DAY_INDEX])
        else:
            month_num = date_object.month
            day_num = date_object.day

        month_name = calendar.month_name[month_num]
        date_str = f"{month_name} {day_num:02d}"

        formatted_temp = format_temp_int(extreme_weather_reading)
        formatted_extreme_value_str = f"{formatted_temp}{unit} on {date_str}"

    else:
        formatted_extreme_value_str = "N/A"

    return formatted_extreme_value_str


def build_color_bar(temperature_in_degrees, ascii_color_code):
    """Builds a single colored ASCII bar based on ASCII code."""
    temperature_in_degrees = max(temperature_in_degrees, MINIMUM_VALUE)

    return f"{ascii_color_code}{'+' * temperature_in_degrees}{RESET_ASCII}"


def get_monthly_chart_lines(month_name, year_str, highest_temps, lowest_temps):
    """Creates formatted string lines for the monthly chart report."""
    monthly_chart_lines = [f"{month_name} {year_str}"]

    for day_index in range(len(highest_temps)):
        day_high = highest_temps[day_index]
        day_low = lowest_temps[day_index]

        if day_high is None or day_low is None:
            continue

        formatted_high = format_temp_int(day_high)
        formatted_low = format_temp_int(day_low)

        high_temp_bar = build_color_bar(formatted_high, RED_ASCII)
        low_temp_bar = build_color_bar(formatted_low, BLUE_ASCII)

        monthly_chart_lines.append(f"{day_index + 1:02d} {high_temp_bar} {day_high}C")
        monthly_chart_lines.append(f"{day_index + 1:02d} {low_temp_bar} {day_low}C")

    return monthly_chart_lines


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

        blue_bar = build_color_bar(min_temp, BLUE_ASCII)
        red_bar = build_color_bar(max_temp - min_temp, RED_ASCII)

        combined_bar = blue_bar.replace(RESET_ASCII, "") + red_bar

        bonus_chart_lines.append(
            f"{day_num:02d} {combined_bar} {min_temp}C-{max_temp}C"
        )

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
        f"{extreme_value_label}: {format_extreme_value(val, date_obj, unit)}"
        for extreme_value_label, val, date_obj, unit in report_configs
    ]

    return extreme_values
