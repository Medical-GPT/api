from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models.model_factory import ModelFactory

modelFactory = ModelFactory()

app = FastAPI()

origins = ["http://localhost:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_json()
            response = modelFactory.consume(message)
            await websocket.send_json({"message": response})
        except WebSocketDisconnect:
            break


# Get the list of models
@app.get("/models")
def get_models():
    return modelFactory.get_models_json()


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
