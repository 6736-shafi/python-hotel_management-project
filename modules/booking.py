from config.db_config import get_connection
from datetime import datetime
from modules.payment import Payment
from utils.logger import setup_logger

# Set up the logger
logger = setup_logger()
class Booking:
    """
    Booking Class

    Manages hotel bookings, including room validation, booking creation, and cancellations (full or partial).
    Uses database connections to fetch and update booking-related data.
    """
    def __init__(self, booking_id, payment_id,room_id, customer_id, check_in, check_out):
        self.booking_id = booking_id
        self.payment_id = payment_id
        self.room_id = room_id
        self.customer_id = customer_id
        self.check_in = check_in
        self.check_out = check_out


    @staticmethod
    def is_Valid_room( ):
        """
            Validates if a room is available for booking.

            Prompts the user to enter a room ID and checks its availability in the database.
            If the room is not available or does not exist, the user is prompted to enter a valid ID.

            Returns:
                str: The valid room ID if available.
        """
        conn = get_connection()
        cursor = conn.cursor()
        while True:
            room_id = input("Enter room ID to book: ")
            # Check if the room exists and is available
            cursor.execute("SELECT is_available FROM rooms WHERE room_id = %s", (room_id,))
            room = cursor.fetchone()

            if room is None:
                logger.warning(f"Room ID {room_id} does not exist.")
                print(f"Room ID {room_id} does not exist. Please enter a valid room ID.")
            elif not room[0]:  # If is_available is False
                print(f"Room ID {room_id} is not available. Please choose another room.")
            else:
                logger.info(f"Room ID {room_id} is available for booking.")
                return room_id
                  




    @staticmethod
    def create_booking( payment_id,days,room_id, customer_id, check_in, check_out):
        """
        Creates a new booking in the database.

        Fetches room price from the database to calculate the total amount for the stay.
        Updates the room status to unavailable after booking.

        Args:
            payment_id (str): ID of the payment made for the booking.
            days (int): Number of days for the stay.
            room_id (str): ID of the booked room.
            customer_id (str): ID of the customer making the booking.
            check_in (str): Check-in date in 'YYYY-MM-DD' format.
            check_out (str): Check-out date in 'YYYY-MM-DD' format.

        Logs:
            Info: Logs successful booking creation and the total amount.

        Prints:
            Success message with the total amount charged for the stay.
        """
        conn = get_connection()
       
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM rooms WHERE room_id = %s", (room_id,))
        price = cursor.fetchone()
        total_amount =price[0]*days
        cursor.execute(
            """
            INSERT INTO bookings (payment_id,room_id, customer_id, check_in, check_out, total_amount) 
            VALUES (%s,%s, %s, %s, %s, %s)
            """,
            (payment_id,room_id, customer_id, check_in, check_out, total_amount)
        )
        
        cursor.execute(f"UPDATE rooms SET is_available=False WHERE room_id={room_id}")
        conn.commit()
        logger.info(f"Creating booking for Customer ID {customer_id} with total amount ${total_amount}.")
        print(f"\n\nBooking created successfully for Customer ID {customer_id} with total amount ${total_amount}.")




    @staticmethod
    def cancel_booking(booking_id):
        """
    Cancels an existing booking, offering both full and partial cancellation options.

    Fetches booking details to determine eligibility for cancellation. Depending on the 
    user's choice, processes either a full or partial cancellation and updates the booking
    and room status accordingly.

    Args:
        booking_id (str): ID of the booking to be cancelled.

    Full Cancellation:
        - Refunds 50% of the total amount.
        - Marks the booking as 'CANCELLED'.

    Partial Cancellation:
        - Prompts the user to enter a new check-out date.
        - Calculates a new total amount based on the adjusted stay duration.
        - Refunds the difference between the original and new total amount.

    Logs:
        - Info: Logs the details of cancellation (full or partial) and refund amounts.
        - Error: Logs any exceptions encountered during the cancellation process.

    Prints:
        - Success or error messages based on the outcome.
        - Refund amount details if applicable.

    Raises:
        Exception: If any error occurs during the cancellation process, it is logged and printed.

    Finally:
        Closes the database connection.
    """
        try:
            conn = get_connection()
            cursor = conn.cursor()

        # Check if the booking exists and its status
            cursor.execute(
                "SELECT status, check_out FROM bookings WHERE booking_id = %s",
                (booking_id,)
            )
            result = cursor.fetchone()

            if result:
                status, check_out = result

             # Fetch room details and total amount
                cursor.execute(
                    "SELECT room_id, total_amount, check_in ,payment_id ,customer_id FROM bookings WHERE booking_id = %s",
                    (booking_id,)
                )
                room = cursor.fetchone()
                room_id = room[0]
                total_amount = room[1]
                check_in_date = room[2]
                payment_id = room[3]
                customer_id= room[4]

                # Check if the booking is eligible for cancellation
                if status == 'CONFIRMED':
                    choice = int(input("\n\n1. Full Cancellation OR 2. Partial Cancellation: "))

                    if choice == 1:
                        # Full cancellation: Refund half of the total amount
                        cursor.execute(
                            """
                            UPDATE bookings
                            SET cancellation_status = 'CANCELLED',
                                total_amount = total_amount / 2,
                                cancellation_timestamp = CURRENT_TIMESTAMP,
                                status = 'CANCELLED'
                            WHERE booking_id = %s
                            """,
                            (booking_id,)
                        )
                        cursor.execute(
                        """
                        UPDATE rooms
                        SET is_available = TRUE
                        WHERE room_id = %s
                        """,
                        (room_id,)
                        )
                        Payment.isRefund(total_amount / 2,payment_id,total_amount / 2)
                        logger.info(f"Full cancellation processed for Booking ID {booking_id}. Refund: {total_amount / 2} to this {customer_id} customer")

                        print(f"Half of the total amount will be refunded to this {customer_id} customer id. Refund: {total_amount / 2}")

                    elif choice == 2:
                        new_check_out = input('\nEnter new check-out date (YYYY-MM-DD): ')
                        new_check_out_date = datetime.strptime(new_check_out, "%Y-%m-%d").date()
                        new_check_in_date= datetime.strptime(str(check_in_date), "%Y-%m-%d").date()

                        # Ensure that 'check_in_date' is used as a date object directly
                        diff = (new_check_out_date - new_check_in_date).days
                        print(f'room_id {room_id}')
                        cursor.execute("SELECT price FROM rooms WHERE room_id = %s", (room_id,))
                        price = cursor.fetchone()
                        print(f'price {price[0]}')

                        # Calculate new total amount based on the shortened stay
                        new_total_amount = price * diff
                        print(f'new_total_amount {new_total_amount}')
                       

                        cursor.execute(
                            """
                            UPDATE bookings
                            SET cancellation_status = 'PARTIAL CANCELLED',
                                total_amount = %s,
                                check_out = %s,
                                cancellation_timestamp = CURRENT_TIMESTAMP,
                                status = 'CANCELLED'
                            WHERE booking_id = %s
                            """,
                            (new_total_amount, new_check_out, booking_id)
                        )
                        cursor.execute(
                        """
                        UPDATE rooms
                        SET is_available = TRUE
                        WHERE room_id = %s
                        """,
                        (room_id,)
                         )
                        refund_amount = float(total_amount) - float(new_total_amount[0])
                        print(f'refund_amount {refund_amount}')
                        Payment.isRefund(new_total_amount,payment_id,refund_amount)
                       
                        logger.info(f"Partial cancellation processed. New total amount: ${new_total_amount}..Refund {refund_amount} to this {customer_id} customer id")
                        print(f"Partial cancellation processed. New total amount: {new_total_amount} .Refund {refund_amount} to this {customer_id} customer id")

                    else:
                        print("Invalid choice. Please select 1 or 2.")

                   

                    conn.commit()
                    logger.info(f"Booking ID {booking_id} has been cancelled successfully.")
                   

                else:
                    print("Booking cannot be cancelled as it is already cancelled or does not exist.")
            else:
                print("No booking found with the provided ID.")

        except Exception as e:
            logger.error(f"An error occurred while cancelling Booking ID {booking_id}: {e}")
            print(f"An error occurred while cancelling Booking ID {booking_id}: {e}")

        finally:
            # Close the connection
            if conn:
                conn.close()
