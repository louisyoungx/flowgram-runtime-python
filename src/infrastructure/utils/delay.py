from typing import Any
import asyncio


async def delay(ms: int) -> None:
    """
    Creates a promise that resolves after a specified time.
    
    Args:
        ms: The time to delay in milliseconds.
        
    Returns:
        A promise that resolves after the specified time.
    """
    await asyncio.sleep(ms / 1000)