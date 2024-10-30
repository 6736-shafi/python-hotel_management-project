class Menu:
    @staticmethod
    def display_menu():
        """
        Displays the main menu options for the hotel booking system.

        This method prints a list of available actions that a user can take,
        including viewing available rooms, booking a room, canceling a booking,
        and viewing booking or cancellation history.

        Returns:
            None

        The menu options displayed include:
            - Viewing available rooms
            - Booking a room
            - Canceling a booking and processing refunds
            - Viewing booking or cancellation history
            - Exiting the application
        """
        print("\n\n1. View Available Rooms")
        print("2. Book a Room")
        print("3. Cancel Booking And Refund")
        print("4. View Booking / Cancellation History")
        print("7. Exit")
        print('\n')