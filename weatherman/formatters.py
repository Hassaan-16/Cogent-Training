import calendar
from datetime import date

from constants import (
    BLUE_ASCII,
    LABEL_HIGHEST,
    LABEL_HUMIDITY,
    LABEL_LOWEST,
    MINIMUM_VALUE,
    NOT_APPLICABLE,
    RED_ASCII,
    RESET_ASCII,
    UNIT_CELSIUS,
    UNIT_PERCENT,
)


class FormatterHelper:
    """Helper class containing static methods for formatting report outputs."""

    @staticmethod
    def _format_chart_header(month_name, year):
        """Formats the header line for a chart."""

        return f"{month_name} {year}"

    @staticmethod
    def _process_daily_bonus_row(daily_measurement):
        """Orchestrates data extraction, formatting, and building for a single row."""
        day_num = daily_measurement.day
        min_temp = FormatterHelper.format_temp_int(
            daily_measurement.minimum_temperature
        )
        max_temp = FormatterHelper.format_temp_int(
            daily_measurement.maximum_temperature
        )

        combined_bar = FormatterHelper.build_combined_color_bar(min_temp, max_temp)

        return FormatterHelper.format_bonus_chart_row(
            day_num, combined_bar, min_temp, max_temp
        )

    @staticmethod
    def format_temp_int(temperature_in_degrees):
        """temperature rounding as integers. None values returned as N/A."""
        if temperature_in_degrees is None:
            return NOT_APPLICABLE

        return int(round(temperature_in_degrees))

    @staticmethod
    def format_extreme_value(
        extreme_weather_reading: int | None,
        date_object: date | None,
        unit: str = UNIT_CELSIUS,
    ) -> str:
        """Return a Formated extreme value or 'N/A' if unavailable"""

        if None in [extreme_weather_reading, date_object]:
            return NOT_APPLICABLE

        month_name = calendar.month_name[date_object.month]
        formatted_temp = FormatterHelper.format_temp_int(extreme_weather_reading)

        return f"{formatted_temp}{unit} on {month_name} {date_object.day:02d}"

    @staticmethod
    def build_color_bar(temperature_in_degrees, ascii_color_code):
        """Builds a single colored ASCII bar based on ASCII code."""
        temperature_in_degrees = max(temperature_in_degrees, MINIMUM_VALUE)

        return f"{ascii_color_code}{'+' * temperature_in_degrees}{RESET_ASCII}"

    @staticmethod
    def build_combined_color_bar(min_temp_int, max_temp_int):
        """Calculates and concatenates the dual-color ASCII bar."""
        blue_bar = FormatterHelper.build_color_bar(min_temp_int, BLUE_ASCII)
        red_bar = FormatterHelper.build_color_bar(
            max_temp_int - min_temp_int, RED_ASCII
        )

        return blue_bar.replace(RESET_ASCII, "") + red_bar

    @staticmethod
    def format_bonus_chart_row(day_num, combined_bar, min_temp, max_temp):
        """Handles the strict string layout for a single bonus chart row."""

        return f"{day_num:02d} {combined_bar} {min_temp}C-{max_temp}C"

    @staticmethod
    def format_chart_row(day_num, bar, temp):
        """Returns formatted string lines for the monthly chart report."""

        return f"{day_num:02d} {bar} {temp}C"

    @staticmethod
    def get_monthly_chart_lines(month_name, year_str, highest_temps, lowest_temps):
        """Creates formatted string lines for the monthly chart report."""
        lines = [f"{month_name} {year_str}"]

        for day_index, (high_temp, low_temp) in enumerate(
            zip(highest_temps, lowest_temps), start=1
        ):
            formatted_high = FormatterHelper.format_temp_int(high_temp)
            formatted_low = FormatterHelper.format_temp_int(low_temp)

            lines.append(
                FormatterHelper.format_chart_row(
                    day_index,
                    FormatterHelper.build_color_bar(formatted_high, RED_ASCII),
                    high_temp,
                )
            )
            lines.append(
                FormatterHelper.format_chart_row(
                    day_index,
                    FormatterHelper.build_color_bar(formatted_low, BLUE_ASCII),
                    low_temp,
                )
            )

        return lines

    @staticmethod
    def get_bonus_chart_lines(daily_temps):
        """return formatted string lines for the combined bonus chart."""
        if not daily_temps.daily_temperature:
            return ["No daily temperatures found to chart."]

        bonus_chart_lines = FormatterHelper.create_bonus_chart_lines(daily_temps)

        return bonus_chart_lines

    @staticmethod
    def create_bonus_chart_lines(daily_temps):
        """Creates complete chart lines for the combined bonus chart."""
        bonus_chart_lines = [
            FormatterHelper._format_chart_header(
                daily_temps.month_name, daily_temps.year
            )
        ]

        for daily in daily_temps.daily_temperature:
            formatted_row = FormatterHelper._process_daily_bonus_row(daily)
            bonus_chart_lines.append(formatted_row)

        return bonus_chart_lines

    @staticmethod
    def get_average_monthly_lines(average_metrics):
        """Builds formatted string lines for the average monthly report."""
        high_temp_avg = FormatterHelper.format_temp_int(
            average_metrics.average_maximum_temperature
        )
        low_temp_avg = FormatterHelper.format_temp_int(
            average_metrics.average_minimum_temperature
        )
        humidity_avg = FormatterHelper.format_temp_int(average_metrics.average_humidity)

        average_monthly_lines = [
            f"Highest Average: {high_temp_avg}C",
            f"Lowest Average: {low_temp_avg}C",
            f"Average Mean Humidity: {humidity_avg}%",
        ]

        return average_monthly_lines

    @staticmethod
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
            f"{extreme_value_label}: {
                FormatterHelper.format_extreme_value(extreme_value, date_obj, unit)
            }"
            for (extreme_value_label, extreme_value, date_obj, unit) in report_configs
        ]

        return extreme_values
