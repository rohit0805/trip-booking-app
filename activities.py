import asyncio
from temporalio import activity
from shared import BookVacationInput

@activity.defn
async def book_car(book_input: BookVacationInput)-> str:
    """
    Book a car activity
    :param
        book_input(BookVacationInput): Input data for booking a car
    :return
        str: Confirmation message
    """
    print(f"Booking car: {book_input.book_car_id}")
    return f"{book_input.book_car_id}"

@activity.defn
async def book_hotel(book_input: BookVacationInput)-> str:
    """
    Book a hotel activity
    :param
        book_input(BookVacationInput): Input data for booking a hotel
    :return
        str: Confirmation message
    """
    await asyncio.sleep(1)
    attempt_info = f"Invoking activity, attempt number: {activity.info().attempt}"
    if activity.info().attempt < 2:
        activity.heartbeat(attempt_info)
        await asyncio.sleep(1)
        raise RuntimeError(f"Hotel service is down. Attempt number: {activity.info().attempt}. Retrying...")

    if "invalid" in book_input.book_hotel_id:
        raise ValueError("Invalid hotel booking, rolling back!")

    print(f"Booking hotel: {book_input.book_hotel_id}")
    return f"{book_input.book_hotel_id}"

@activity.defn
async def book_flight(book_input: BookVacationInput)-> str:
    """
    Book a flight activity
    :param
        book_input: Input data for booking a flight
    :return
        str: Confirmation message
    """
    print(f"Booking flight: {book_input.book_flight_id}")
    return f"{book_input.book_flight_id}"

@activity.defn
async def undo_book_car(book_input: BookVacationInput)-> str:
    """
    Undo a book car activity
    :param
        book_input(BookVacationInput): Input data for undoing a book car
    :return
        str: Confirmation message
    """
    print(f"Undoing book car: {book_input.book_car_id}")
    return f"{book_input.book_car_id}"

@activity.defn
async def undo_book_hotel(book_input: BookVacationInput)-> str:
    """
    Undo a book hotel activity
    :param
        book_input: Input data for undoing a book hotel
    :return
        str: Confirmation message
    """
    print(f"Undoing book hotel: {book_input.book_hotel_id}")
    return f"{book_input.book_hotel_id}"

@activity.defn
async def undo_book_flight(book_input: BookVacationInput)-> str:
    """
    Undo a book flight activity
    :param
        book_input: Input data for undoing a book flight
    :return
        str: Confirmation message
    """
    print(f"Undoing book flight: {book_input.book_flight_id}")
    return f"{book_input.book_flight_id}"