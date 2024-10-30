import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import setup_logger  # Assuming you have a logger setup

# Initialize logger
logger = setup_logger()

class Email:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        """Initialize SMTP server details."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    @staticmethod
    def send_email(  receiver_email,  message):
        
        """
        Sends an email to the specified receiver.

        Args:
            receiver_email (str): The email address of the recipient.
            message (str): The content of the email message to be sent.

        Raises:
            SMTPAuthenticationError: If authentication with the SMTP server fails.
            SMTPException: If there is an issue with sending the email.
        """
        try:
            # Send the email
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            subject='Taj Hotel : registered successfully.'
            msg = "Subject: " + subject + '\n' + message
            server.login('mdshafiuddin935@gmail.com','ikqu unzb mnlt atik')
            server.sendmail('mdshafiuddin935@gmail.com',receiver_email,msg) 
            
           
            logger.info(f"Email sent successfully to {receiver_email}")
            print(f"Email sent successfully to {receiver_email}")

        except smtplib.SMTPAuthenticationError:
            logger.error("Authentication failed. Please check your email or password.")
            print("Authentication failed. Please check your email or password.")

        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email: {e}")
            print(f"An error occurred: {e}")

        finally:
            # Close the server connection
            server.quit()
            logger.info("SMTP server connection closed.")


    
  
