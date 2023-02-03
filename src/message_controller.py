from responses import responses


def get_message_response(message):
    [message_text] = message
    # model.predict(message_text)
    response = responses.pop(0)
    responses.append(response)
    return response
