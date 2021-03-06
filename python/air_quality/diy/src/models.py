import logging

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from .database import Base
from .lib import gmail

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    aqi_alert_notifications = relationship(
        "AQIAlertNotification", back_populates="user"
    )

    def send_welcome_email(self):
        # Here you would send the welcome email when the user is created
        gmail.send(message=f"Welcome {self.email}!", subject="Welcome!", to=self.email)

    def send_updated_email(self, previous_email):
        # Here you would send an email to let the user know of the updated email
        gmail.send(
            message=(
                f"Your email has been updated to {self.email}. If you didn't make that "
                "change, please reach at to us here: support@notivize.com"
            ),
            subject="Your email has been updated",
            to=previous_email,
        )

        # And also ask them to verify their new email
        gmail.send(
            message=(
                "Hi, please verify your email by clicking this link: "
                f"<a href='https://notivize.com/verify?email={self.email}'>Verify</a>"
            ),
            subject="Verify your email",
            to=self.email,
        )


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    zone = Column(String, index=True)
    aqi = Column(Integer)

    aqi_alert_notifications = relationship(
        "AQIAlertNotification", back_populates="sensor"
    )


class AQIAlert(Base):
    __tablename__ = "aqi_alerts"

    id = Column(Integer, primary_key=True, index=True)
    threshold = Column(Integer)
    level = Column(
        String, ChoiceType({"warning": "Warning", "info": "Info", "alert": "Alert"})
    )

    aqi_alert_notifications = relationship(
        "AQIAlertNotification", back_populates="alert"
    )


class AQIAlertNotification(Base):
    __tablename__ = "aqi_alert_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    alert_id = Column(Integer, ForeignKey("aqi_alerts.id"))

    user = relationship("User", back_populates="aqi_alert_notifications")
    sensor = relationship("Sensor", back_populates="aqi_alert_notifications")
    alert = relationship("AQIAlert", back_populates="aqi_alert_notifications")

    def maybe_send_notification(self):
        if self.sensor.aqi <= self.alert.threshold:
            return

        gmail.send(
            message=(
                f"{self.alert.level.title()}! Air quality index at {self.sensor.city}, "
                f"{self.sensor.zone} is above its threshold ({self.alert.threshold}): "
                f"{self.sensor.aqi}"
            ),
            subject=f"Air Quality Index {self.alert.level.title()}!",
            to=self.user.email,
        )
