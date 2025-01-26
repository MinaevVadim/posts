import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from log_config import add_logger

logger = add_logger(__name__)


class SenderEmail:
    """Mail sending class"""

    def __init__(
        self,
        message: str,
        email_from: str,
        email_to: str,
        subject: str,
        sub_type: str = "plain",
    ):
        self._msg = MIMEMultipart()
        self._msg["From"] = email_from
        self._msg["To"] = email_to
        self._msg["Subject"] = subject
        self._message = message
        self._server = self._init_server
        self._msg.attach(MIMEText(self._message, sub_type))

    def login_user(self, password):
        """User login method"""
        self._server.login(self._msg["From"], password)

    @property
    def _init_server(self):
        """Method for creating an SMTP client session object"""
        server = smtplib.SMTP("smtp.gmail.com: 587")
        server.starttls()
        return server

    def send_message(self):
        """The method of sending the message"""
        self._server.sendmail(self._msg["From"], self._msg["To"], self._msg.as_string())
        logger.info("Successfully sent email to %s:" % (self._msg["To"]))
        self._server.quit()
