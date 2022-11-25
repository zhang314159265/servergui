import socket
import dataclasses
from asyncio.queues import Queue
import functools
import asyncio
import websockets
import os
import json
import hashlib
import optparse

@dataclasses.dataclass
class Task:
    path: str
    file_size = None
    md5sum = None

    def __post_init__(self):
        assert self.file_size is None
        self.file_size = os.path.getsize(self.path)
        with open(self.path, "rb") as f:
            self.md5sum = hashlib.md5(f.read()).hexdigest()

    # TODO: add a generic method to dump a dataclass as json
    def to_json(self):
        return json.dumps({"path": self.path, "file_size": self.file_size, "md5sum": self.md5sum})

@functools.lru_cache()
def get_queue():
    return Queue()

async def add_task(task):
    if isinstance(task, str):
        task = Task(task)

    assert isinstance(task, Task)
    print(f"Add task to the queue: {task.path}")
    await get_queue().put(task)

async def handle_tcp_conn(reader, writer):
    data = await reader.read(1024)
    path = data.decode()
    print(f"TCP server received message {path}")
    if not os.path.exists(path):
        print(f"Invalid path {path}")
        return
    writer.close()
    await add_task(path)

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
            metadata_str = task.to_json()
            await ws.send(len(metadata_str).to_bytes(8, "big"))
            await ws.send(metadata_str)

            with open(task.path, "rb") as f:
                while data := f.read(1024):  # write at most 1024 bytes once
                    await ws.send(data)

            print(f"ws_handler finished task {task.path}")
        except websockets.ConnectionClosedOK:
            break

    print("Exit handler")

async def ws_server():
    print("Start ws_server")
    async with websockets.serve(ws_handler, "", 1346):
        await asyncio.Future()  # run forever

async def main():
    usage = """
        usage: sgserver [path...]

        Paths specified on the command line will be put into the queue directly.
    """
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()

    for path in args:
        await add_task(path) 

    await asyncio.gather(
        ws_server(),
        tcp_server()
    )

asyncio.run(main())
print("bye")
