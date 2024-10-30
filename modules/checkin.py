from datetime import datetime

class CheckIn:
    """
    CheckIn Class

    Handles operations related to check-in and check-out, including validating dates 
    and calculating the duration of a stay.
    """
    @staticmethod
    def get_stay_duration():
        """
        Prompts the user for check-in and check-out dates, validates them, and calculates the stay duration.

        Returns:
            tuple: A tuple containing:
                - duration (int): The number of days between check-in and check-out.
                - check_in_date (datetime.date): The validated check-in date.
                - check_out_date (datetime.date): The validated check-out date.

        Raises:
            ValueError: If the input date format is incorrect.
        """
        # Get and validate check-in date
        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()

        while True:
            # Get and validate check-out date
            check_out = input("Enter valid check-out date (YYYY-MM-DD): ")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

            if check_out_date >= check_in_date:
                break
            else:
                print("Check-out date must be later than the check-in date. Please try again.")

        # Calculate the difference in days
        duration = (check_out_date - check_in_date).days
        return int(duration), check_in_date, check_out_date  # Return the diff and dates if needed


