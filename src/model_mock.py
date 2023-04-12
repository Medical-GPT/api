from responses import responses
import asyncio


async def predict_response(message):
    response = responses.pop(0)
    responses.append(response)

    await asyncio.sleep(1)

    return response
