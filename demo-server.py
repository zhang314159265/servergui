import asyncio
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    print(f"Server got data: {data}")
    reply = f"Data received as: {data}!"
    await websocket.send(reply)

start_server = websockets.serve(handler, "localhost", 1346)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
