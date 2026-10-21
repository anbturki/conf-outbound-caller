import base64
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from uuid import UUID

from shared.logger import logger


def json_encoder(obj):
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode("utf-8")
    elif isinstance(obj, list):
        return [json_encoder(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: json_encoder(value) for key, value in obj.items()}
    elif isinstance(obj, set):
        return list(json_encoder(item) for item in obj)
    elif isinstance(obj, tuple):
        return list(json_encoder(item) for item in obj)
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, int):
        return int(obj)

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def json_dumps(obj):
    return json.dumps(obj, default=json_encoder)


# Decode json as well, if there as a type such as dataclass assigned, convert it to data class
def json_loads(obj, cls=None):
    try:
        if cls is None:
            logger.info(f"Decoding JSON: {obj}")
            return json.loads(obj)
        else:
            logger.info(f"Decoding JSON: {obj}")
            return json.loads(obj, object_hook=lambda d: cls(**d))
    except Exception as e:
        logger.error(f"Error decoding JSON: {e}")
        raise ValueError(f"Error decoding JSON: {e}")
