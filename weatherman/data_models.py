from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherReading:
    """data structure for holding each weather reading."""

    date: date | None
    maximum_temperature: float | None
    minimum_temperature: float | None
    maximum_humidity: float | None
    mean_humidity: float | None


@dataclass
class AverageResults:
    """data structure for holding the average calculations results"""

    average_maximum_temperature: float | None
    average_minimum_temperature: float | None
    average_humidity: float | None


@dataclass
class ExtremeResults:
    """results for yearly extreme values"""

    maximum_temperature: float | None
    maximum_temperature_date: date | None
    minimum_temperature: float | None
    minimum_temperature_date: date | None
    maximum_humidity: float | None
    maximum_humidity_date: date | None


@dataclass
class DailyTemperature:
    """holds the chart for a single day"""

    day: int
    maximum_temperature: float | None
    minimum_temperature: float | None


@dataclass
class ChartResults:
    """holds the chart data for the month"""

    month_name: str
    year: str
    daily_temperature: list[DailyTemperature]
