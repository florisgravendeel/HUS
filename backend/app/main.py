import random
from typing import Optional

from fastapi import FastAPI
import uvicorn
import asyncio
from xknx import XKNX
from xknx.devices import Light

app = FastAPI()


@app.get("/")
def read_root():
    return {"Helloooo": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
#    asyncio.run(test())
    uvicorn.run(app, port=8000, host="0.0.0.0")

async def spookymode():
    print("hi!")

    xknx = XKNX()
    await xknx.start()
    light = Light(xknx,
                  name='HelloWorldLight',
                  group_address_switch='0/0/6')
    await asyncio.sleep(0.2)
    random_n = random.random()
    if random_n < 0.1:
        await light.set_off()
    else:
        await light.set_on()
    await xknx.stop()
    await spookymode()

#asyncio.run(spookymode())
