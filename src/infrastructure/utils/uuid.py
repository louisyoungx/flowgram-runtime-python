import uuid as uuid_lib
from typing import Any


def uuid() -> str:
    """
    Generates a random UUID v4.
    
    Returns:
        A string representation of a random UUID v4.
    """
    return str(uuid_lib.uuid4())