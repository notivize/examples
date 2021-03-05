import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def on_startup() -> None:
    format_ = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format_, level=logging.INFO, datefmt="%H:%M:%S")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=user)
    user.send_welcome_email()
    return user


@app.patch("/users/", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserPatch, db: Session = Depends(get_db)):
    existing_user_with_new_email = crud.get_user_by_email(db, email=user.email)
    if existing_user_with_new_email:
        raise HTTPException(
            status_code=400, detail="Email already registered by another user"
        )
    db_user = crud.get_user(db, user_id)
    previous_email = db_user.email
    updated_user = crud.update_user(
        db=db,
        user_id=user_id,
        update_data=user.dict(exclude_unset=True),
    )
    updated_user.send_updated_email(previous_email)
    return updated_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/sensors/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    return crud.create_sensor(db=db, sensor=sensor)


@app.patch("/sensors/{sensor_id}", response_model=schemas.Sensor)
def update_sensor(
    sensor_id: int, sensor: schemas.SensorPatch, db: Session = Depends(get_db)
):
    updated_sensor = crud.update_sensor(
        db=db,
        sensor_id=sensor_id,
        update_data=sensor.dict(exclude_unset=True),
    )
    for aqi_alert_notification in updated_sensor.aqi_alert_notifications:
        aqi_alert_notification.maybe_send_notification()

    return updated_sensor


@app.get("/sensors/", response_model=List[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sensors(db, skip=skip, limit=limit)


@app.get("/sensors/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@app.post("/aqi_alerts/", response_model=schemas.AQIAlert)
def create_aqi_alert(aqi_alert: schemas.AQIAlertCreate, db: Session = Depends(get_db)):
    return crud.create_aqi_alert(db=db, aqi_alert=aqi_alert)


@app.get("/aqi_alerts/", response_model=List[schemas.AQIAlert])
def read_aqi_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_aqi_alerts(db, skip=skip, limit=limit)


@app.get("/aqi_alerts/{aqi_alert_id}", response_model=schemas.AQIAlert)
def read_aqi_alert(aqi_alert_id: int, db: Session = Depends(get_db)):
    db_aqi_alert = crud.get_aqi_alert(db, aqi_alert_id=aqi_alert_id)
    if db_aqi_alert is None:
        raise HTTPException(status_code=404, detail="AQIAlert not found")
    return db_aqi_alert


@app.post("/aqi_alert_notifications/", response_model=schemas.AQIAlertNotification)
def create_aqi_alert_notification(
    aqi_alert_notification: schemas.AQIAlertNotificationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_aqi_alert_notification(
        db=db, aqi_alert_notification=aqi_alert_notification
    )


@app.get("/aqi_alert_notifications/", response_model=List[schemas.AQIAlertNotification])
def read_aqi_alert_notifications(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_aqi_alert_notifications(db, skip=skip, limit=limit)


@app.get(
    "/aqi_alert_notifications/{aqi_alert_notification_id}",
    response_model=schemas.AQIAlertNotification,
)
def read_aqi_alert_notification(
    aqi_alert_notification_id: int, db: Session = Depends(get_db)
):
    db_aqi_alert_notification = crud.get_aqi_alert_notification(
        db, aqi_alert_notification_id=aqi_alert_notification_id
    )
    if db_aqi_alert_notification is None:
        raise HTTPException(status_code=404, detail="AQIAlertNotification not found")
    return db_aqi_alert_notification
