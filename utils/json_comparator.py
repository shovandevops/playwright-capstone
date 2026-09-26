# utils/json_comparator.py
from typing import Any, Tuple, Optional

def deep_compare(actual: Any, expected: Any, path: str = "root") -> Tuple[bool, Optional[str]]:
    """
    Recursively compares two JSON structures and reports the mismatch path.
    
    :param actual: Actual JSON object/dict/list/primitive
    :param expected: Expected JSON object/dict/list/primitive
    :param path: Internal dot-notation path tracking
    :return: Tuple of (is_match: bool, error_message: str or None)
    """
    # Type mismatch check
    if type(actual) is not type(expected):
        return False, f"Type mismatch at '{path}': Expected {type(expected).__name__}, got {type(actual).__name__}"

    # Dictionary comparison
    if isinstance(actual, dict):
        # Check keys presence
        if set(actual.keys()) != set(expected.keys()):
            missing = set(expected.keys()) - set(actual.keys())
            extra = set(actual.keys()) - set(expected.keys())
            details = []
            if missing:
                details.append(f"missing keys: {missing}")
            if extra:
                details.append(f"extra keys: {extra}")
            return False, f"Key mismatch at '{path}': {', '.join(details)}"

        # Recurse values
        for key in expected:
            matched, err = deep_compare(actual[key], expected[key], path=f"{path}.{key}")
            if not matched:
                return False, err

    # List comparison
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            return False, f"List length mismatch at '{path}': Expected {len(expected)}, got {len(actual)}"
        for idx, (act_item, exp_item) in enumerate(zip(actual, expected)):
            matched, err = deep_compare(act_item, exp_item, path=f"{path}[{idx}]")
            if not matched:
                return False, err

    # Primitive values comparison
    else:
        if actual != expected:
            return False, f"Value mismatch at '{path}': Expected '{expected}', got '{actual}'"

    return True, None