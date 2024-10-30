from config.db_config import get_connection
from datetime import datetime
from utils.logger import setup_logger

# Set up the logger
logger = setup_logger()

class History:
    """
    A class for managing customer booking history.

    This class provides methods to view booking history for a given customer ID.
    """
    @staticmethod
    def view_history(customer_id):
        """
        Fetches and displays the booking history for a specified customer.

        Args:
            customer_id (int): The ID of the customer whose booking history is to be retrieved.

        Returns:
            None

        Raises:
            Exception: If an error occurs while fetching booking history or executing the SQL query.

        This method connects to the database, retrieves the bookings for the given customer ID,
        and prints the booking details in a user-friendly format. The booking details include
        the booking ID, room ID, nights booked, check-in and check-out dates, status of the booking,
        booking time, total amount, cancellation status, and cancellation timestamp.

        Logs the following information:
            - Successful retrieval of booking history.
            - Error messages if no bookings are found or if an error occurs.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Fetch bookings for the given customer ID
            cursor.execute("SELECT * FROM bookings WHERE customer_id = %s", (customer_id,))
            data = cursor.fetchall()

            # Check if there are any bookings for the customer
            if data:
                logger.info(f"Fetched booking history for Customer ID: {customer_id}")
                print('\n')
                print(f"\nBooking history for Customer ID: {customer_id}\n")
                for booking in data:
                    # Unpack values for better readability
                    (booking_id, room_id, nights, customer_id, check_in, check_out, 
                    status, booking_time, amount, cancellation_status, 
                    cancellation_timestamp) = booking

                    # Format dates to make them user-friendly
                    check_in_str = check_in.strftime("%d-%b-%Y") 
                    check_out_str = check_out.strftime("%d-%b-%Y")  
                    booking_time_str = booking_time.strftime("%d-%b-%Y %H:%M:%S")
                    cancellation_timestamp_str = (
                        cancellation_timestamp.strftime("%d-%b-%Y %H:%M:%S") 
                        if cancellation_timestamp else "N/A"
                    )

                    # Pretty print the booking details
                    print(f"Booking ID: {booking_id}")
                    print(f"Room ID: {room_id}")
                    print(f"Nights: {nights}")
                    print(f"Check-in: {check_in_str}")
                    print(f"Check-out: {check_out_str}")
                    print(f"Status: {status}")
                    print(f"Booking Time: {booking_time_str}")
                    print(f"Total Amount: ${amount}")
                    print(f"Cancellation Status: {cancellation_status}")
                    print(f"Cancellation Timestamp: {cancellation_timestamp_str}")
                    print('-' * 40)

            else:
                logger.error(f"An error occurred while fetching booking history for Customer ID {customer_id}:")
                logger.info(f"No bookings found for Customer ID: {customer_id}")
                print(f"\n\nNo bookings found for Customer ID: {customer_id}")

        except Exception as e:
            logger.error(f"An error occurred while fetching booking history for Customer ID {customer_id}: {e}")
            print(f"\n\nAn error occurred while fetching booking history: {e}")

        finally:
            if conn:
                conn.close()


