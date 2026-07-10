import data_models
import calendar
from constants import DEFAULT_VALUE, DATE_PARTS_LIMIT, DATE_MONTH_INDEX, DATE_YEAR_INDEX


def _get_average(values):
    """Helper function to DRY up average calculations."""
    return sum(values) / len(values) if values else DEFAULT_VALUE


def _get_or_default(value):
    """Helper function to safely handle missing daily data."""
    return value if value is not None else DEFAULT_VALUE


def _extract_year_and_month(date_str):
    """SRP Helper: Extracts the year string and month name from a date."""
    clean_date = date_str.replace("/", "-")
    parts = clean_date.split("-")

    if len(parts) < DATE_PARTS_LIMIT:
        return "", "Unknown"

    year_str = parts[DATE_YEAR_INDEX]
    try:
        month_num = int(parts[DATE_MONTH_INDEX])
        month_name = calendar.month_name[month_num]
    except ValueError:
        month_name = "Unknown"

    return year_str, month_name


def calculate_average_monthly(record):
    """calculate the average monthly max/min temperature and mean humidity"""
    max_temps = [
        row.maximum_temperature for row in record if row.maximum_temperature is not None
    ]
    min_temps = [
        row.minimum_temperature for row in record if row.minimum_temperature is not None
    ]
    mean_hums = [row.mean_humidity for row in record if row.mean_humidity is not None]

    return data_models.AverageResults(
        _get_average(max_temps), _get_average(min_temps), _get_average(mean_hums)
    )


def calculate_monthly_report(record):
    """gets the monthly min and max temperatures"""
    highest_temps = [_get_or_default(row.maximum_temperature) for row in record]
    lowest_temps = [_get_or_default(row.minimum_temperature) for row in record]

    return highest_temps, lowest_temps


def calculate_chart_data(record):
    """Parses data into a ChartResults object for bonus mixed charts."""
    daily_temps = []
    year_str = ""
    month_name = ""

    for row in record:
        if not row.date:
            continue

        if not year_str:
            year_str, month_name = _extract_year_and_month(row.date)

        try:
            clean_date = row.date.replace("/", "-")
            clean_day = int(clean_date.split("-")[-DATE_MONTH_INDEX])

            max_temp = _get_or_default(row.maximum_temperature)
            min_temp = _get_or_default(row.minimum_temperature)

            daily_temps.append(
                data_models.DailyTemperature(clean_day, max_temp, min_temp)
            )
        except (ValueError, IndexError):
            continue

    return data_models.ChartResults(month_name, year_str, daily_temps)


def _evaluate_extreme(current_record, record_date, new_value, new_date, find_max=True):
    """DRY Helper: Compares and returns the new extreme value and its date."""
    if new_value is None:
        return current_record, record_date

    if current_record is None:
        return new_value, new_date

    is_new_record = (
        (new_value > current_record) if find_max else (new_value < current_record)
    )

    if is_new_record:
        return new_value, new_date

    return current_record, record_date


def calculate_extreme_values(record):
    """Gets the max temperature, min temperature and max humidity with their dates"""
    highest_temp, highest_date = None, ""
    lowest_temp, lowest_date = None, ""
    max_humidity, humidity_date = None, ""

    for row in record:
        highest_temp, highest_date = _evaluate_extreme(
            highest_temp, highest_date, row.maximum_temperature, row.date, find_max=True
        )
        lowest_temp, lowest_date = _evaluate_extreme(
            lowest_temp, lowest_date, row.minimum_temperature, row.date, find_max=False
        )
        max_humidity, humidity_date = _evaluate_extreme(
            max_humidity, humidity_date, row.maximum_humidity, row.date, find_max=True
        )

    return data_models.ExtremeResults(
        maximum_temperature=highest_temp,
        maximum_temperature_date=highest_date,
        minimum_temperature=lowest_temp,
        minimum_temperature_date=lowest_date,
        maximum_humidity=max_humidity,
        maximum_humidity_date=humidity_date,
    )
