import logging
import re
from config.db_config import get_connection
from modules.email import Email
from modules.room import Room
from utils.exceptions import RegistrationError, LoginError


class Customer:
    """
    Customer Class

    Handles customer operations such as registration, validation, and login. 
    Also manages interactions with the database and sends registration confirmation emails.
    """
    def __init__(self, first_name, last_name, email, phone_number):
        """
        Initializes a new Customer instance.

        Args:
            first_name (str): The customer's first name.
            last_name (str): The customer's last name.
            email (str): The customer's email address.
            phone_number (str): The customer's phone number.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    
    
    @staticmethod
    def register():
        """
        Handles customer registration by collecting user input, validating data, 
        saving customer information to the database, and sending a confirmation email.

        Returns:
            Customer: A Customer instance representing the registered user.

        Raises:
            RegistrationError: If an exception occurs during the registration process.
        """
        try:
            
            first_name = ""
            while not first_name or not Customer.is_valid_name(first_name):
                first_name = input("First Name (2-52 characters, only alphabets): ").strip()
                if not Customer.is_valid_name(first_name):
                    print("Invalid first name. It should contain only alphabets, be 2-52 characters long, and may include spaces.")

            
            last_name = ""
            while not last_name or not Customer.is_valid_name(last_name):
                last_name = input("Last Name (2-52 characters, only alphabets): ").strip()
                if not Customer.is_valid_name(last_name):
                    print("Invalid last name. It should contain only alphabets, be 2-52 characters long, and may include spaces.")

            
            email = ""
            while not email or not Customer.is_valid_email(email):
                email = input("Email: ").strip()
                if not Customer.is_valid_email(email):
                    print("Invalid email format. Please try again.")

            
            if Customer.is_email_registered(email):
                print("Email is already registered. Please try logging in.")
                return 

            
            password = ""
            while not password or not Customer.is_valid_password(password):
                password = input("Password (at least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character, no spaces): ").strip()
                if not Customer.is_valid_password(password):
                    print("Invalid password. It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, one special character, and no spaces.")

            
            phone_number = ""
            while not phone_number or not Customer.is_valid_phone(phone_number):
                phone_number = input("Phone Number (must contain 10 digits, can include spaces, dashes, parentheses, and a country code): ").strip()
                if not Customer.is_valid_phone(phone_number):
                    print("Invalid phone number format. It should contain 10 digits and may include spaces, dashes, parentheses, and a country code.")

            
            conn = get_connection()
            cursor = conn.cursor()
        
            cursor.execute(
                """
                INSERT INTO customers (first_name, last_name, email, password, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (first_name, last_name, email, password, phone_number)
            )
            conn.commit()
            print(f"\nCustomer {first_name} {last_name} registered successfully.")

            # Fetch available rooms and send a confirmation email
            available_rooms = Room.fetch_rooms()
            msg = (
                f"Thanks {first_name} {last_name} for registering with us.\n"
                f"Available Rooms: {available_rooms}"
            )
            Email.send_email(email, msg)

            logging.info(f"Customer {first_name} {last_name} registered successfully.")
            return Customer(first_name, last_name, email, phone_number)

        except Exception as e:
            logging.error(f"Registration failed: {e}")
            raise RegistrationError("Registration failed.") from e

        finally:
            if conn:
                conn.close()

    @staticmethod
    def is_email_registered(email):
        """
        Checks if an email is already registered in the database.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if the email is registered, False otherwise.
        """
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers WHERE email = %s", (email,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0

    
    @staticmethod
    def is_valid_name(name):
        """
        Validates a name to ensure it contains only alphabets and spaces, and is 2-52 characters long.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        regex = r'^[A-Za-z\s]{2,52}$'
        return re.match(regex, name) is not None

    @staticmethod
    def is_valid_email(email):
        """
        Validates an email address using regex.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        """Validate email format using regex."""
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(regex, email) is not None

    @staticmethod
    def is_valid_password(password):
        """
        Validates a password to ensure it meets security requirements.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        """Validate password: 8 characters long, at least 1 uppercase, 1 lowercase, 1 digit, 1 special character, no spaces."""
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[^\s]{8,}$'
        return re.match(regex, password) is not None

    @staticmethod
    def is_valid_phone(phone_number):
        """
        Validates a phone number, ensuring it contains exactly 10 digits 
        and supports common formats with spaces, dashes, and parentheses.

        Args:
            phone_number (str): The phone number to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        """Validate phone number format (10 digits, allows spaces, dashes, parentheses, and country code)."""
        # +1-800-555-1234
        # +44 20 1234 5678
        # 1(800)555-1234
        # 800.555.1234
        # +91 1234567890
        regex = r'^\+?\d{1,3}?[-.\s]?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$'
        return re.match(regex, phone_number) is not None and len(re.sub(r'\D', '', phone_number)) == 10

    @staticmethod
    def login():
        """
        Handles customer login by validating email and password against the database.

        Returns:
            tuple: A tuple containing user information if login is successful.

        Raises:
            LoginError: If an error occurs during the login process.
        """
        while True:
            try:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT customer_id, first_name, last_name, email, phone_number FROM customers WHERE email = %s AND password = %s", 
                    (email, password)
                )

                # Validate the user credentials with the Snowflake database
                result = cursor.fetchone()
                if result:
                    logging.info(f"User {email} logged in successfully.")
                    return result  # Return user information upon successful login
                else:
                    print("\nInvalid credentials or user not found. please enter valid email and password")
                    logging.warning(f"Failed login attempt for email: {email}")

            except Exception as e:
                logging.error("An error occurred during login", exc_info=True)
                raise LoginError("Login failed. Please check your credentials.") from e
            finally:
                # Close the cursor and connection
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    
      
       
    
    







































