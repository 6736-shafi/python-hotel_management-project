from config.db_config import get_connection
from datetime import datetime
from utils.logger import setup_logger
logger = setup_logger()

class Payment:
    """
    A class to handle payment processing and refunding in a hotel booking system.

    This class provides methods for processing payments for room bookings
    and managing refunds for payments made by customers.
    """
    def __init__(self, room_id, amount):
        self.room_id = room_id  
        self.amount = amount  
        self.total_amount = 0 
    @staticmethod
    def process_payment(amount, room_id):
        """
        Processes the payment for a given room ID.

        This method fetches the price of the specified room from the database,
        prompts the user for payment, and records the payment in the database.

        Parameters:
            amount (float): The base amount for the booking.
            room_id (int): The ID of the room to be booked.

        Returns:
            int: The payment ID if the payment is processed successfully.

        Raises:
            ValueError: If the user input for the payment amount is invalid.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Fetch room price from the database
            cursor.execute("SELECT price FROM rooms WHERE room_id = %s", (room_id,))
            price = cursor.fetchone()

            if price is None:
                print(f"No room found with room_id: {room_id}")
                return

            total_amount = amount * price[0]  # Calculate the required payment
            print(f"\n\nThe total amount for your stay is ${total_amount}.")

            while True:
                try:
                    # Prompt user for payment
                    paid_amount = float(input(f"Enter payment amount (at least ${total_amount}): "))

                    # Check if the paid amount is sufficient
                    if paid_amount >= total_amount:
                        print(f"\n\nProcessing payment of ${paid_amount}...")
                        print("Payment successful! Thank you.")

                        # Insert payment record into the payments table
                        cursor.execute(
                            """
                            INSERT INTO payments (room_id, amount, payment_date, isRefund)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (room_id, paid_amount, datetime.now(), False)
                        )
                        cursor.execute(
                            """
                            SELECT payment_id 
                            FROM payments 
                            ORDER BY payment_date DESC 
                            LIMIT 1
                            """
                        )
                        latest_payment_id = cursor.fetchone()[0]
                        conn.commit()
                        logger.info(f"Payment recorded successfully with ID: {latest_payment_id}")
                        print("Payment recorded successfully.")
                        return latest_payment_id 
                    else:
                        print(f"Insufficient payment! You still need to pay at least ${total_amount}.")
                except ValueError:
                    print("Invalid input! Please enter a valid amount.")

        except Exception as e:
            logger.error(f"An error occurred while processing payment: {e}")
            print(f"An error occurred: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()




                
    @staticmethod
    def isRefund(amount, payment_id,refunded_amount):
        """
        Processes a refund for a given payment ID.

        This method updates the specified payment record in the database to indicate
        that it has been refunded.

        Parameters:
            amount (float): The new amount to be recorded for the refund.
            payment_id (int): The ID of the payment to be refunded.
            refunded_amount (float): The total refunded amount.

        Returns:
            None

        Raises:
            Exception: If an error occurs while updating the payment record.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Update the amount and set isRefund to true
            cursor.execute(
                """
                UPDATE payments
                SET amount = %s, isRefund = TRUE,
                REFUNDED_AMOUNT = %s
                WHERE payment_id = %s
                """,
                (amount, refunded_amount,payment_id)
            )
            
            # Check if any rows were affected
            if cursor.rowcount > 0:
                print(f"Payment ID {payment_id} updated successfully with new amount ${amount}.")
                conn.commit()  
            else:
                print(f"No payment found with ID {payment_id}.")
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback() 
        finally:
            cursor.close()
            conn.close()

