import asyncio

def run_in_new_loop(coroutine):
    new_loop = asyncio.new_event_loop()
    try:
        return new_loop.run_until_complete(coroutine)
    finally:
        new_loop.close()