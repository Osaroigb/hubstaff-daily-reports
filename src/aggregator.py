from collections import defaultdict
from typing import List, Dict, Tuple

def aggregate_activities(
    daily_activities: List[dict],
    users: Dict[int, dict],
    projects: Dict[int, dict]
) -> Tuple[Dict[int, Dict[int, int]], Dict[int, str], Dict[int, str]]:
    """
    Aggregates total tracked time by (project_id, user_id).
    
    Returns:
      - A nested dict: { project_id: { user_id: total_tracked_seconds, ... }, ... }
      - user_map: { user_id: user_name }
      - project_map: { project_id: project_name }
    """
    # Initialize aggregator as a nested dict
    aggregator = defaultdict(lambda: defaultdict(int))

    # Build name maps
    user_map = {}
    for user_id, user_data in users.items():
        user_map[user_id] = user_data.get("name", f"User {user_id}")

    project_map = {}
    for project_id, proj_data in projects.items():
        project_map[project_id] = proj_data.get("name", f"Project {project_id}")

    # Iterate over daily activities, sum up "tracked" time
    for item in daily_activities:
        user_id = item["user_id"]
        project_id = item["project_id"]
        tracked_seconds = item.get("tracked", 0)
        aggregator[project_id][user_id] += tracked_seconds

    return aggregator, user_map, project_map