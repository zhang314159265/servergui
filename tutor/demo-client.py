import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:1346") as websocket:
        for i in range(3):
            await websocket.send("hello")
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(test())
