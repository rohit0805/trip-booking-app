import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from temporalio.client import Client
from pydantic import BaseModel

from shared import TASK_QUEUE_NAME, BookVacationInput
from workflows import BookingWorkflow


class BookRequest(BaseModel):
    name: str
    attempts: int
    car: str
    hotel: str
    flight: str

def generate_unique_username(name: str)-> str:
    return f"{name.replace(' ', '-').lower()}-{str(uuid.uuid4().int)[:6]}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect("localhost:7233")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/book")
async def book_vacation(payload: BookRequest):
    user_id = generate_unique_username(payload.name)

    input_data = BookVacationInput(
        attempts= payload.attempts,
        book_user_id= user_id,
        book_car_id = payload.car,
        book_hotel_id = payload.hotel,
        book_flight_id = payload.flight
    )

    result = await app.state.temporal_client.execute_workflow(
        BookingWorkflow.run,
        input_data,
        id=user_id,
        task_queue=TASK_QUEUE_NAME,
    )

    return {
        "user_id": user_id,
        "result": result
    }