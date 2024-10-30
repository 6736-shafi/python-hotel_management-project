import logging
from modules.customer import Customer
from modules.room import Room
from modules.history import History
from modules.booking import Booking
from utils.logger import setup_logger
from modules.payment import Payment
from modules.checkin import CheckIn
from modules.menu import Menu
"""
Hotel Booking System

This application manages the hotel booking process, including user registration, login, room management, 
booking, payment processing, and customer booking history. It follows a menu-driven approach, allowing users 
to interact with different functionalities.

Modules:
- logging: For logging system events and errors.
- Customer: Handles user registration and login.
- Room: Manages room-related operations.
- History: Displays customer booking history.
- Booking: Manages bookings, including creation and cancellation.
- Payment: Processes payments for room bookings.
- CheckIn: Handles stay duration details (check-in and check-out).
- Menu: Displays the menu for user interaction.
- setup_logger: Initializes logging configurations.

Functions:
- main(): Entry point of the application. Manages user flow, including registration, login, room selection, 
  booking, payment, and viewing history through a menu system.

Usage:
1. User chooses between registration and login.
2. Upon login, the user can:
   - View available rooms.
   - Book a room by selecting a valid room ID and processing payment.
   - Cancel an existing booking using a booking ID.
   - View booking history.
   - Exit the system.
3. Errors are logged for troubleshooting.

Exception Handling:
- Any unexpected errors are logged using the logging module.

Entry Point:
- The `main()` function is executed when the script is run directly.
"""

def main():
    setup_logger()
    logging.info("Starting the Hotel Booking System...")
    try:
        user=None 
        while True:
            ch=input('\n 1.registration   2. login \n\n')
            if ch =='1':
                Customer.register()
            else: 
                user = Customer.login()
                break
       

        if user:
            while True:
                Menu.display_menu()
                choice = input("Select an option: ")
                if choice == '1':
                    Room.fetch_rooms_from_db()
                elif choice == '2':
                    room_id = Booking.is_Valid_room()
                    days, check_in, check_out=CheckIn.get_stay_duration()
                    if check_in == check_out:
                        days=1
                    payment_id = Payment.process_payment(days,room_id)
                    Booking.create_booking( payment_id,days,room_id, user[0], check_in, check_out)
                elif choice == '3':
                    booking_id = input("Enter your Booking ID for Cancelation : ")
                    Booking.cancel_booking(booking_id)
                elif choice == '4':
                    customer_id = user[0]
                    History.view_history(customer_id)
                elif choice == '7':
                    logging.info("Exiting the Hotel Booking System.")
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            logging.error("Login failed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()








































































































