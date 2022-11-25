""" a debugging client. """

import asyncio
import websockets
import json
import hashlib

EXPECT_LEN = 0
EXPECT_META = 1
EXPECT_PAYLOAD = 2

async def main():
    async with websockets.connect("ws://localhost:1346") as ws:
        buffered = bytes()
        state = EXPECT_LEN
        len_metadata = 0
        metadata = {}
        payload = None
        file_size = 0
        while True:
            response = await ws.recv()
            if isinstance(response, str):
                response = response.encode()

            buffered += response
            print(f"# buffered bytes {len(buffered)}")
            if state == EXPECT_LEN:
                if len(buffered) >= 8:
                    len_metadata = int.from_bytes(buffered[:8], "big")
                    buffered = buffered[8:]
                    state = EXPECT_META
                    print(f"Got metadata length {len_metadata}")
            elif state == EXPECT_META:
                if len(buffered) >= len_metadata:
                    metadata = json.loads(buffered[:len_metadata].decode())
                    file_size = metadata["file_size"]
                    buffered = buffered[len_metadata:]
                    state = EXPECT_PAYLOAD
                    print(f"Got metadata {metadata}")
            elif state == EXPECT_PAYLOAD:
                if len(buffered) >= file_size:
                    payload = buffered[:file_size]
                    buffered = buffered[file_size:]
                    state = EXPECT_LEN
                    actual_md5 = hashlib.md5(payload).hexdigest()
                    expected_md5 = metadata["md5sum"]
                    print(f"md5 match: {actual_md5 == expected_md5}")
            else:
                # TODO: why raise AssertionError does not have any effect?
                print(f"Invalid state {state}")


asyncio.run(main())
print("bye")
