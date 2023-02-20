from model import predict_response


async def get_message_response(message):
    [message_text] = message

    response = await predict_response(message_text)
    # TODO: add empathic rewriting here

    return response
