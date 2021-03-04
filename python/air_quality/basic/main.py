import http
import os

import click
import requests

APPLICATION_ID = os.getenv("APPLICATION_ID", "7c697f8c-0acf-42cb-924a-b88032b4e221")
EVENT_FLOW_ID = os.getenv("EVENT_FLOW_ID", "1ff218d5-c85a-422d-9723-dd7c352d0b15")
NOTIVIZE_API_URL = os.getenv("NOTIVIZE_API_URL", "https://events-api.notivize.com")


def aqi_notify(unique_id, aqi_value, email, first_name):
    """Function that calls Notivize to decide if a notification should be sent."""
    response = requests.post(
        f"{NOTIVIZE_API_URL}/applications/{APPLICATION_ID}/event_flows/{EVENT_FLOW_ID}/events",  # noqa: E501
        json={
            "aqi_value": aqi_value,
            "email": email,
            "first_name": first_name,
            "unique_id": unique_id,
        },
    )

    assert response.status_code == http.HTTPStatus.ACCEPTED


@click.command()
@click.option(
    "--email",
    "-e",
    prompt="Your email address",
    help="Enter the email to send the test notification to",
)
@click.option(
    "--first_name",
    "-f",
    prompt="Your first name",
    help="First name of the person receiving the notification",
)
@click.option(
    "--sensor-id",
    "-s",
    default="san_francisco_mission_and_9th",
    help="Made up sensor id, can be anything!",
)
def main(email, first_name, sensor_id):
    # Simulate a range of AQI values using a simple loop.
    for aqi_value in range(145, 155):
        # Get the current air quality, usually from an API call
        print(f"Current AQI for sensor {sensor_id} is {aqi_value}")
        # stream the current aqi values and other info to Notivize
        aqi_notify(sensor_id, aqi_value, email, first_name)


if __name__ == "__main__":
    main()
