import os
import json

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from volatile import LookupTable


source_dir = os.environ['SERVER_DATA_DIR']

source = LookupTable(source_dir)

app = FastAPI()


class RequestData(BaseModel):
    key: str
    value: str


@app.get("/{key}")
async def get(key: str):
    try:
        value = await source.get(key)

        if value:
            return Response(content=value, media_type="text/plain")

    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/")
async def set(request_data: RequestData):
    await source.insert(key=request_data.key, value=request_data.value)

    return Response(
        content=json.dumps(request_data.dict()),
        media_type="application/json"
    )
