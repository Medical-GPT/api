from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from message_model import Message
from message_controller import get_message_response

app = FastAPI()

origins = ["http://localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/message")
def message(message: Message):
    response = get_message_response(message)
    return {"message": response}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            message = await websocket.receive_json()
            response = get_message_response(message)
            await websocket.send_json({"message": response})
        except WebSocketDisconnect:
            break


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
