import logging
from config.db_config import get_connection
from modules.customer import Customer

def insert_customer_to_db(first_name, last_name, email, phone_number):
    """Insert a new customer into the Snowflake database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, phone_number)
        )
        conn.commit()
        logging.info(f"Inserted customer: {first_name} {last_name}.")
    except Exception as e:
        logging.error(f"Error inserting customer: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def validate_user_credentials(email, password):
    """Validate user credentials against the Snowflake database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT first_name, last_name, email, phone_number FROM customers WHERE email = %s AND password = %s", 
            (email, password)  # Ensure that passwords are securely handled (hashed, etc.)
        )
        result = cursor.fetchone()
        if result:
            return Customer(result[0], result[1], result[2], result[3])  # Create and return Customer object
        else:
            return None
    except Exception as e:
        logging.error(f"Error validating credentials: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
