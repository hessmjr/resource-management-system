from re import compile, match
from typing import Any

# Pre-compile regex patterns for performance
LAT_REGEX = compile(r"^-?(90(\.0+)?|[1-8]?[0-9]\.\d{1,6})$")
LNG_REGEX = compile(r"^-?(180(\.0+)?|1[0-7][0-9]\.\d{1,6}|[0-9]?[0-9]\.\d{1,6})$")
COST_REGEX = compile(r"^\d+(\.\d{2})?$")
ALPHANUMERIC_REGEX = compile(r"^[a-zA-Z0-9\s\-\.]+$")


def validate_coordinates(lat: str, lng: str) -> bool:
    # Latitude: -90 to 90, longitude: -180 to 180, must have decimal places
    return bool(match(LNG_REGEX, lng) and match(LAT_REGEX, lat))


def validate_cost_format(cost: str) -> bool:
    # Must have exactly 2 decimal places or be a whole number
    return bool(match(COST_REGEX, cost))


def validate_cost_amount(cost: str) -> bool:
    try:
        return float(cost) >= 0.0
    except ValueError:
        return False


def validate_alphanumeric_format(value: str) -> bool:
    # Allow letters, numbers, spaces, hyphens, and periods only
    return bool(match(ALPHANUMERIC_REGEX, value))


def validate_id_in_list(id_str: str, valid_items: list[tuple[Any, ...]]) -> bool:
    if not id_str.isdigit():
        return False

    item_id = int(id_str)
    valid_ids = {item[0] for item in valid_items}

    return item_id in valid_ids
