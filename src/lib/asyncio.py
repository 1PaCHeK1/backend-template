import asyncio
import os


def new_event_loop() -> asyncio.AbstractEventLoop:
    if os.name == "posix":
        import uvloop  # noqa: PLC0415

        return uvloop.new_event_loop()
    return asyncio.new_event_loop()
