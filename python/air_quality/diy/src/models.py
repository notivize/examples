import logging

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
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

        # Here you would setup your channel integration, for example:
        # mailchimp, sendgrid, twilio, etc.
        logger.warning(
            "\n\n"
            f"To: {self.user.email}\n"
            f"Subject: Air Quality Index {self.alert.level.title()}!\n"
            f"{self.alert.level.title()}! Air quality index at {self.sensor.city}, "
            f"{self.sensor.zone} is above its threshold ({self.alert.threshold}): "
            f"{self.sensor.aqi}"
            "\n\n"
        )
