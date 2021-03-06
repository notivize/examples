# -*- coding: utf-8 -*-
import logging
import smtplib

from ..config import settings

logger = logging.getLogger(__name__)


def send(message: str, subject: str, to: str) -> None:
    """Send an email message via an ssl gmail smtp server.

    Note that you have to enable "less secure apps" to make it work.
    Or you can also generate an "app password".
    """
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()
        server_ssl.login(settings.gmail_user, settings.gmail_password)
        server_ssl.sendmail(from_addr=settings.gmail_user, to_addrs=[to], msg=message)
        server_ssl.close()
    except Exception:
        # We just log the error and do nothing. We don't want our app to fail because
        # notifications are not working... 😉
        logger.exception("Something went wrong sending an email via gmail smtp! 📧 😱")
