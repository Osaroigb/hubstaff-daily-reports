import sys
from config import load_config
from api_client import HubstaffAPIClient
from aggregator import aggregate_activities
from report_generator import generate_html_report

def main():
    try:
        config = load_config()

        app_token = config["app_token"]
        email = config["email"]
        password = config["password"]
        organization_id = config["organization_id"]
        report_day = config["report_day"]

        client = HubstaffAPIClient(app_token, email, password)
        client.signin()

        daily_activities, users, projects = client.fetch_daily_activities(
            organization_id=organization_id,
            report_day=report_day
        )

        aggregator, user_map, project_map = aggregate_activities(
            daily_activities, users, projects
        )

        html_report = generate_html_report(aggregator, user_map, project_map)
        print(html_report)

    except Exception as e:
        sys.stderr.write(f"Error generating daily report: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()