from datetime import timedelta


def convert_to_timedelta(delta: str) -> timedelta:
    """Convert a string to a timedelta.

    Args:
        delta (str): The string to convert.

    Returns:
        timedelta: The timedelta.
    """
    if delta.endswith("d"):
        return timedelta(days=int(delta[:-1]))
    elif delta.endswith("h"):
        return timedelta(hours=int(delta[:-1]))
    elif delta.endswith("m"):
        return timedelta(minutes=int(delta[:-1]))
    elif delta.endswith("s"):
        return timedelta(seconds=int(delta[:-1]))
    elif delta.endswith("ms"):
        return timedelta(milliseconds=int(delta[:-2]))
    elif delta.endswith("us"):
        return timedelta(microseconds=int(delta[:-2]))
    else:
        raise ValueError(f"Invalid time delta: {delta}")
