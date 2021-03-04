from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, update_data: dict) -> models.User:
    query = db.query(models.User).filter(models.User.id == user_id)
    query.update(update_data)
    db.commit()
    return query.first()


def get_sensor(db: Session, sensor_id: int) -> Optional[models.Sensor]:
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Sensor]:
    return db.query(models.Sensor).offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: schemas.SensorCreate) -> models.Sensor:
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def update_sensor(db: Session, sensor_id: int, update_data: dict) -> models.Sensor:
    query = db.query(models.Sensor).filter(models.Sensor.id == sensor_id)
    query.update(update_data)
    db.commit()
    return query.first()


def get_aqi_alerts(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.AQIAlert]:
    return db.query(models.AQIAlert).offset(skip).limit(limit).all()


def create_aqi_alert(db: Session, aqi_alert: schemas.AQIAlertCreate) -> models.AQIAlert:
    db_aqi_alert = models.AQIAlert(**aqi_alert.dict())
    db.add(db_aqi_alert)
    db.commit()
    db.refresh(db_aqi_alert)
    return db_aqi_alert


def get_aqi_alert_notifications(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.AQIAlertNotification]:
    return db.query(models.AQIAlertNotification).offset(skip).limit(limit).all()


def create_aqi_alert_notification(
    db: Session, aqi_alert_notification: schemas.AQIAlertNotificationCreate
) -> models.AQIAlertNotification:
    db_aqi_alert_notification = models.AQIAlertNotification(
        **aqi_alert_notification.dict()
    )
    db.add(db_aqi_alert_notification)
    db.commit()
    db.refresh(db_aqi_alert_notification)
    return db_aqi_alert_notification
