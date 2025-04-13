import requests

class HubstaffAPIClient:
    """
    A simple client for interacting with the custom Hubstaff-like API.
    """
    BASE_URL = "https://mutator.reef.pl"

    def __init__(self, app_token: str, email: str, password: str):
        self.app_token = app_token
        self.email = email
        self.password = password
        self.auth_token = None


    def signin(self) -> None:
        """
        Authenticates the user with the API using email & password.
        """
        url = f"{self.BASE_URL}/v635/people/signin"

        headers = {
            "AppToken": self.app_token
        }

        data = {
            "email": self.email,
            "password": self.password
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        json_data = response.json()
        self.auth_token = json_data["auth_token"]


    def fetch_daily_activities(self, organization_id: int, report_day: str):
        """
        Fetches the daily activities for the given organization on the specified day.
        Returns a tuple: (daily_activities_list, users_list, projects_list, tasks_list)
        """
        if not self.auth_token:
            raise ValueError("Auth token not set. Call signin() first.")

        # Build the date range
        start_of_day = f"{report_day}T00:00:00Z"
        end_of_day = f"{report_day}T23:59:59Z"

        all_daily_activities = []
        all_users = {}
        all_projects = {}

        page_start_id = 0
        page_limit = 100

        while True:
            url = f"{self.BASE_URL}/v635/organization/{organization_id}/work/day"

            headers = {
                "AppToken": self.app_token,
                "AuthToken": self.auth_token,
                "DateStart": start_of_day,
                "PageStartId": str(page_start_id),
                "PageLimit": str(page_limit),
                "Include": "users,projects"
            }

            params = {
                "date[stop]": end_of_day
            }

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()

            daily_activities = data.get("daily_activities", [])
            all_daily_activities.extend(daily_activities)

            # store them in dictionaries keyed by ID to unify duplicates across pages.
            for user in data.get("users", []):
                all_users[user["id"]] = user

            for project in data.get("projects", []):
                all_projects[project["id"]] = project

            # Check pagination
            pagination = data.get("pagination", {})
            next_page_id = pagination.get("next_page_start_id")

            if not next_page_id:
                break

            page_start_id = next_page_id

        return all_daily_activities, all_users, all_projects