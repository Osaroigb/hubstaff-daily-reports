import os
import configparser
from datetime import datetime, timedelta, timezone

def load_config(config_path: str = None) -> dict:
    """
    Loads configuration settings from an INI file using configparser.
    Returns a dictionary with the relevant configuration values.
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.ini")

    parser = configparser.ConfigParser()
    parser.read(config_path)
    hubstaff = parser["hubstaff"]

    app_token = hubstaff.get("APP_TOKEN")
    email = hubstaff.get("EMAIL")
    password = hubstaff.get("PASSWORD")
    organization_id = hubstaff.get("ORGANIZATION_ID")

    config = {
        "app_token": app_token,
        "email": email,
        "password": password,
        "organization_id": organization_id,
        "report_day": get_report_day()
    }
    
    return config


def get_report_day() -> str:
    """
    Get yesterday's date in ISO format (YYYY-MM-DD).
    """
    # Defaults to yesterday
    yest = datetime.now(timezone.utc) - timedelta(days=1)
    return yest.strftime('%Y-%m-%d')