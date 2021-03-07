import logging
from http import HTTPStatus

import requests
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from .config import settings
from .database import Base

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    aqi_alert_notifications = relationship(
        "AQIAlertNotification", back_populates="user"
    )

    def send_welcome_email(self):
        response = requests.post(
            f"{settings.notivize_api_url}/applications/8060536a-b20a-4692-9794-075ff079d144/event_flows/d53b14aa-1882-48d6-9fd6-ac8c7fc61f99/events",  # noqa: E501
            json={
                "email": self.email,
                "lifecycle_stage": "create",
                "user_id": self.id,
            },
            headers={"Authorization": f"Bearer {settings.notivize_api_key}"},
        )
        assert response.status_code == HTTPStatus.ACCEPTED
        self.send_verify_email()

    def send_verify_email(self):
        response = requests.post(
            f"{settings.notivize_api_url}/applications/8060536a-b20a-4692-9794-075ff079d144/event_flows/b39dcc00-8331-4e34-9a53-ae9280e6110c/events",  # noqa: E501
            json={
                "email": self.email,
                "lifecycle_stage": "update",
            },
            headers={"Authorization": f"Bearer {settings.notivize_api_key}"},
        )

        assert response.status_code == HTTPStatus.ACCEPTED

    def send_updated_email(self, previous_email):
        response = requests.post(
            f"{settings.notivize_api_url}/applications/8060536a-b20a-4692-9794-075ff079d144/event_flows/b156d4a0-b40f-4562-9517-e074573e7676/events",  # noqa: E501
            json={
                "email": previous_email,
                "email_has_changed": previous_email != self.email,
                "new_email": self.email,
                "user_id": self.id,
            },
            headers={"Authorization": f"Bearer {settings.notivize_api_key}"},
        )
        assert response.status_code == HTTPStatus.ACCEPTED

        self.send_verify_email()


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
        response = requests.post(
            f"{settings.notivize_api_url}/applications/8060536a-b20a-4692-9794-075ff079d144/event_flows/bb0ada8d-c8db-4804-9baf-fa0d0e147a77/events",  # noqa: E501
            json={
                "phone": self.user.phone,
                "aqi_alert_notification_id": self.id,
                "alert_level": self.alert.level.title(),
                "aqi_greater_than_threshold": self.sensor.aqi > self.alert.threshold,
                "aqi": self.sensor.aqi,
                "city": self.sensor.city,
                "zone": self.sensor.zone,
            },
            headers={"Authorization": f"Bearer {settings.notivize_api_key}"},
        )
        assert response.status_code == HTTPStatus.ACCEPTED
