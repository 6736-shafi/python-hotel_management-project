from config.db_config import get_connection
from utils.logger import setup_logger
logger = setup_logger()


class Room:
    def __init__(self, room_id, room_type, price, is_available=True):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.is_available = is_available

    @staticmethod
    def fetch_rooms_from_db():
        """
        Fetches and displays available rooms from the database.

        This method connects to the database, retrieves all available rooms,
        and prints their details.

        Returns:
            None
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE is_available = True")
        logger.info("Fetched available rooms from the database.")
        print('\n')
        print("room_id roomType price Availability")
        data= cursor.fetchall()
        for i in data:
            print(i)


    @staticmethod
    def fetch_rooms():
        """
        Fetches available rooms from the database.

        This method connects to the database and returns a list of all available rooms.

        Returns:
            list: A list of tuples, each representing an available room.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE is_available = True")
        l=[]
        data= cursor.fetchall()
        for i in data:
            l.append(i)
        return l
