# Do It Yourself

Let's face it... Nobody ain't got time for that!

## Overview

This example shows you how hard it can be to get notifications right, even for simple things.

### Database schema

![Database schema](assets/db_schema.png)

### Setup

We assume that you have a [virtual environment](https://docs.python.org/3/tutorial/venv.html) setup.
Then, open up your favorite terminal and `cd` to `examples/python/air_quality/basic`.

```bash
pip install -r requirements.txt
```

## Tutorial

This tutorial will showcase 4 different notifications:
1. Get a welcome message when a user is created
2. Get an alert when a sensor has an AQI value above the threshold of an alert
3. Get an email that our email has been changed
4. Get an email to verify our new email

### 1. Start server

![Start server](assets/1-start_server.png)

### 2. How to open a section in the explorer view to submit an api request

![Open post user api section](assets/2-open_section.png)

### 3. Create a user

![Create user](assets/3-user_created.png)

### 4. Create a sensor

![Create sensor](assets/4-create_sensor.png)

### 5 Create aqi alert

![Create aqi alert](assets/5-create_aqi_alert.png)

### 6. Create aqi alert notification

![Create aqi alert notification](assets/6-create_aqi_alert_notification.png)

### 7. Trigger aqi alert

![Trigger aqi alert](assets/7-trigger_aqi_alert.png)

### 8. Update email

![Update email](assets/8-update_email.png)


## Explore on your own

```bash
uvicorn src.api:app
```

You should get something like:

![Run server](assets/run_server.png)

Then you can explore the api (`cmd + click` to open video link in new tab):

[<img src="https://cdn.loom.com/sessions/thumbnails/0ed0095ccc75489d89dc67c72ed711d9-with-play.gif">](https://www.loom.com/share/0ed0095ccc75489d89dc67c72ed711d9)

## Reset

You can start from scratch by simply deleting the `diy.db` file.
