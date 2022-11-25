import socket
import dataclasses
from asyncio.queues import Queue
import functools
import asyncio
import websockets

@dataclasses.dataclass
class Task:
    path: str

@functools.lru_cache()
def get_queue():
    return Queue()

async def add_task(task):
    print(f"Add task to the queue: {task.path}")
    await get_queue().put(task)

async def handle_tcp_conn(reader, writer):
    data = await reader.read(1024)
    data = data.decode()
    print(f"TCP server received message {data}")
    writer.close()
    task = Task(path=data)
    await add_task(task)

async def tcp_server():
    print("Start tcp_server")
    server = await asyncio.start_server(
        handle_tcp_conn, "localhost", 1345)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()

async def ws_handler(ws, path):
    """
    TODO: can not handle mutliple concurrent websocket clients properly. The tasks
    will just be randomly split by different ws clients.
    """
    print("Enter handler")
    while True:
        try:
            task = await get_queue().get()
            print(f"ws_handler get task {task.path}")
            await ws.send(task.path)
        except websockets.ConnectionClosedOK:
            break

    print("Exit handler")

async def ws_server():
    print("Start ws_server")
    async with websockets.serve(ws_handler, "", 1346):
        await asyncio.Future()  # run forever

async def main():
    await asyncio.gather(
        ws_server(),
        tcp_server()
    )

asyncio.run(main())
print("bye")
