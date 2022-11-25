""" a debugging client. """

import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:1346") as ws:
        while True:
            response = await ws.recv()
            print(f"Got {response}")

asyncio.run(main())
print("bye")
