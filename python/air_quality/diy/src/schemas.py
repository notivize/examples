from typing import List, Optional

from pydantic import BaseModel


class AQIAlertNotificationBase(BaseModel):
    user_id: int
    sensor_id: int
    alert_id: int


class AQIAlertNotificationCreate(AQIAlertNotificationBase):
    pass


class AQIAlertNotification(AQIAlertNotificationBase):
    id: int

    class Config:
        orm_mode = True


class SensorBase(BaseModel):
    city: str
    zone: str
    aqi: int


class SensorPatch(BaseModel):
    aqi: int


class SensorCreate(SensorBase):
    pass


class Sensor(SensorBase):
    id: int

    class Config:
        orm_mode = True


class AQIAlertBase(BaseModel):
    threshold: int
    level: str


class AQIAlertCreate(AQIAlertBase):
    pass


class AQIAlert(AQIAlertBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    phone: str


class UserCreate(UserBase):
    pass


class UserPatch(BaseModel):
    email: Optional[str]
    phone: Optional[str]


class User(UserBase):
    id: int
    aqi_alert_notifications: List[AQIAlertNotification] = []

    class Config:
        orm_mode = True
