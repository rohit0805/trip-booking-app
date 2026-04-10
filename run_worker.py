import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import (
    book_car,
    book_hotel,
    book_flight,
    undo_book_hotel,
    undo_book_flight,
    undo_book_car
)

from shared import TASK_QUEUE_NAME
from workflows import BookingWorkflow

# Used during shutdown so the process can stop cleanly on Ctrl+C.
interrupt_event = asyncio.Event()

async def main():
    """
    Connect to the Temporal server and start polling for workflow/activity tasks.
    """
    # Create a client connection to the local Temporal dev server.
    client = await Client.connect("localhost:7233")

    # A worker is the long-running process that listens on a task queue and
    # executes the workflows and activities registered here.
    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[BookingWorkflow],
        activities=[
            book_car,
            book_hotel,
            book_flight,
            undo_book_car,
            undo_book_hotel,
            undo_book_flight,
        ]
    )
    print("\n Worker started, ctrl+c to exit\n")

    # This blocks while the worker keeps polling Temporal for new tasks.
    await worker.run()
    try:
        # Wait here until the process receives an interrupt signal.
        await interrupt_event.wait()
    finally:
        print("\n Shutting down the worker\n")

if __name__ == "__main__":
    # Run the async main() function using the current event loop.
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        # On Ctrl+C, signal shutdown and allow async generators to close.
        print("\n Interrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
