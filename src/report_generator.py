from typing import Dict

def generate_html_report(
    aggregator: Dict[int, Dict[int, int]],
    user_map: Dict[int, str],
    project_map: Dict[int, str]
) -> str:
    """
    Generates an HTML table string that shows time spent (in HH:MM) per (project, user).
      - Rows are projects
      - Columns are users
    """
    # gather all user_ids and project_ids that actually appear in aggregator
    all_project_ids = sorted(aggregator.keys())

    # build a set of user_ids from the aggregator to ensure we only show relevant columns
    all_user_ids = set()

    for project_id in aggregator:
        for user_id in aggregator[project_id]:
            all_user_ids.add(user_id)

    all_user_ids = sorted(all_user_ids)

    # check for "no data"
    if not all_project_ids or not all_user_ids:
        return build_no_data_html()

    # build the HTML table
    html_parts = []
    html_parts.append("<html>")
    html_parts.append("<head><meta charset='UTF-8'><title>Daily Report</title></head>")
    html_parts.append("<body>")
    html_parts.append("<h2>Daily Time Report</h2>")
    html_parts.append("<table border='1' cellspacing='0' cellpadding='4'>")

    # header row
    html_parts.append("<tr>")
    html_parts.append("<th>Project</th>")

    for user_id in all_user_ids:
        user_name = user_map.get(user_id, f"User {user_id}")
        html_parts.append(f"<th>{user_name}</th>")

    html_parts.append("</tr>")

    # data rows
    for project_id in all_project_ids:
        project_name = project_map.get(project_id, f"Project {project_id}")
        html_parts.append("<tr>")

        # first cell: Project name
        html_parts.append(f"<td>{project_name}</td>")

        # next cells: time for each user
        for user_id in all_user_ids:
            total_seconds = aggregator[project_id].get(user_id, 0)
            time_str = format_time(total_seconds)
            html_parts.append(f"<td>{time_str}</td>")

        html_parts.append("</tr>")

    html_parts.append("</table>")
    html_parts.append("</body></html>")

    return "".join(html_parts)


def format_time(seconds: int) -> str:
    """
    Converts an integer number of seconds to HH:MM format.
    """
    hours = seconds // 3600
    remainder = seconds % 3600
    minutes = remainder // 60

    return f"{hours:02d}:{minutes:02d}"


def build_no_data_html() -> str:
    """
    Returns a simple HTML page indicating that no users or projects
    had time logged for the period.
    """
    html_parts = []
    html_parts.append("<html>")
    html_parts.append("<head><meta charset='UTF-8'><title>No Data</title></head>")
    html_parts.append("<body>")
    html_parts.append("<h2>Daily Time Report</h2>")
    html_parts.append("<p>No time was tracked for this period.</p>")
    html_parts.append("</body></html>")

    return "".join(html_parts)