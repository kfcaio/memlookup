import os

import msgpack
import aiofiles
import asyncio


class LookupTable:
    def __init__(self, path: str):
        self.source_dir = path
        self.loop = asyncio.get_event_loop()

    async def insert(self, key: str, value: str):
        path = os.path.join(self.source_dir, key)

        packed = msgpack.packb(value)

        async with aiofiles.open(path, 'wb+') as f:
            await f.write(packed)

    async def get(self, key: str):
        path = os.path.join(self.source_dir, key)

        try:
            async with aiofiles.open(path, 'rb') as f:
                content = await f.read()

            return msgpack.loads(content)
        
        except IOError:
            raise KeyError(key)
