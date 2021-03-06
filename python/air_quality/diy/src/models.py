import logging
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from sqlalchemy_utils import ChoiceType

from .database import Base

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
        logging.info(f"Welcome {self.email}!")

    def send_updated_email(self, previous_email):
        # Here you would send an email to let the user know of the updated email
        logging.info(
            f"To: {previous_email}\n"
            "Subject: Your email has been updated\n"
            f"Body: Your email has been updated to {self.email}. If you didn't make "
            "that change, please reach at to us here: support@notivize.com\n"
        )
        # And also ask them to verify their new email
        logging.info(
            f"To: {self.email}\n"
            "Subject: Verify your email\n"
            f"Body: Hi, please verify your email by clicking this link: "
            "<a href='https://notivize.com/verify?email={self.email}'>Verify</a>\n"
        )


class AQI(Base):
    __tablename__ = "aqi_values"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    value = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="aqis")


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    zone = Column(String, index=True)
    aqi = Column(Integer)

    aqi_alert_notifications = relationship(
        "AQIAlertNotification", back_populates="sensor"
    )
    aqi_values = relationship(
        "AQIAlertNotification", back_populates="sensor", lazy="dynamic"
    )

    @classmethod
    def current_aqi_value(cls, db: Session, sensor_id: int):
        current_aqi_value = (
            db.query(AQI.value)
            .filter(AQI.sensor_id == sensor_id)
            .order_by(AQI.created_at.desc())
            .first()
        )
        return current_aqi_value.value if current_aqi_value else None

    aqis = relationship("AQI", back_populates="sensor")


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

    def maybe_send_notification(self, db: Session, previous_aqi_value):
        # If the previous aqi was already above the threshold we don't want to send
        # a notification again
        if previous_aqi_value and previous_aqi_value > self.alert.threshold:
            return

        # If the new aqi is under the threshold, don't send a notification

        current_aqi_value = Sensor.current_aqi_value(db, self.sensor_id)
        if not current_aqi_value or current_aqi_value <= self.alert.threshold:
            return

        # Here you would setup your channel integration, for example:
        # mailchimp, sendgrid, twilio, etc.
        logger.warning(
            "\n\n"
            f"To: {self.user.email}\n"
            f"Subject: Air Quality Index {self.alert.level.title()}!\n"
            f"{self.alert.level.title()}! Air quality index at {self.sensor.city}, "
            f"{self.sensor.zone} is above its threshold ({self.alert.threshold}): "
            f"{current_aqi_value}"
            "\n\n"
        )
