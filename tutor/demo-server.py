import asyncio
import websockets

async def handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
            print(f"Server got data: {data}")
            reply = f"Data received as: {data}!"
            await websocket.send(reply)
        except websockets.ConnectionClosedOK:
            break

    print("Exit handler")

# NOTE: if calling `websockets.serve(handler, "localhost", 1346)` instead, the server would
# only accept local connections.
start_server = websockets.serve(handler, "", 1346)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
