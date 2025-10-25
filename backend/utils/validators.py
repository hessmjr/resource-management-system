from re import compile, match


def validate_coordinates(lat: str, lng: str) -> bool:
    # Latitude: -90 to 90, longitude: -180 to 180, must have decimal places
    lat_regex = compile(r"^-?(90(\.0+)?|[1-8]?[0-9]\.\d{1,6})$")
    long_regex = compile(r"^-?(180(\.0+)?|1[0-7][0-9]\.\d{1,6}|[0-9]?[0-9]\.\d{1,6})$")
    return bool(match(long_regex, lng) and match(lat_regex, lat))


def validate_cost_format(cost: str) -> bool:
    # Must have exactly 2 decimal places or be a whole number
    cost_regex = compile(r"^\d+(\.\d{2})?$")
    return bool(match(cost_regex, cost))


def validate_cost_amount(cost: str) -> bool:
    try:
        return float(cost) >= 0.0
    except ValueError:
        return False


def validate_model_format(model: str) -> bool:
    # Allow letters, numbers, spaces, hyphens, and periods only
    model_regex = compile(r"^[a-zA-Z0-9\s\-\.]+$")
    return bool(match(model_regex, model))


def validate_esf_id(esf_id: str, valid_esfs: list) -> bool:
    if not esf_id.isdigit():
        return False

    esf_id = int(esf_id)

    for esf in valid_esfs:
        if esf_id in esf:
            return True

    return False


def validate_cost_id(cost_id: str, valid_costs: list) -> bool:
    if not cost_id.isdigit():
        return False

    cost_id = int(cost_id)

    for cost in valid_costs:
        if cost_id in cost:
            return True

    return False


def validate_capability_format(capability: str) -> bool:
    # Allow letters, numbers, spaces, hyphens, and periods only
    capability_regex = compile(r"^[a-zA-Z0-9\s\-\.]+$")
    return bool(match(capability_regex, capability))
