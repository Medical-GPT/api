from fastapi import FastAPI
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
