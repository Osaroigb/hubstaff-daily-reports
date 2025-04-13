# Hubstaff Daily Reports

**Table of Contents**  
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation & Setup](#installation--setup)  
5. [Configuration](#configuration)  
6. [Cron Deployment](#cron-deployment)  
7. [Running the Script Manually](#running-the-script-manually)  
8. [Testing](#testing)  
9. [Troubleshooting](#troubleshooting)  
10. [License](#license)  

---

## Project Overview

This **Hubstaff Daily Reports** project provides a **Python-based utility** that fetches and aggregates time-tracking data from a Hubstaff-like API for each user and project within a single organization. The result is an **HTML table** (showing hours spent) that can be **redirected** to a file automatically each day via **cron**.

### Why This Project?

- **Automates** daily generation of an HTML report, so managers can quickly see who worked on which projects and how much time was spent.
- **Configuration-driven**—no need to run queries by hand or read the script code if you’re just deploying.
- **Easily integrable** with any system’s scheduler (cron, systemd, etc.) and minimal external dependencies.

---

## Features

1. **Daily Aggregation**: Grabs time entries for each user and project for “yesterday” (by default) or a configurable date.  
2. **HTML Report**: Outputs a tabular breakdown of time tracked (in hours and minutes), sorted by project (rows) and user (columns).  
3. **Side-Loaded User/Project Names**: Automatically maps user IDs and project IDs to their human-readable names.  
4. **Simple Configuration**: All settings (API tokens, org IDs, etc.) live in a single `config.ini`.  
5. **One-Command Deployment**: `deploy.sh` sets up a virtual environment, installs dependencies, and schedules the daily cron job.

---

## Prerequisites

- **Python 3.7+** (Recommended: Python 3.9 or higher)  
- **pip** package manager  
- **(Optional) cron** or another system scheduler, if you want automatic daily reporting.

---

## Installation & Setup

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/Osaroigb/hubstaff-daily-reports.git
   cd hubstaff-daily-reports
   ```

2. **Create and Edit `config.ini`**:  
   A sample `config.ini` is provided. Fill in the `[hubstaff]` section with your:
   - `app_token` (Hubstaff-like app token)
   - `email` and `password`
   - `organization_id`  

3. **Install Dependencies (Manually)**:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   This step ensures all necessary libraries (like `requests`) are installed in your virtual environment.

---

## Configuration

A typical `config.ini` example:

```ini
[hubstaff]
app_token = YOUR_APP_TOKEN
email = YOUR_EMAIL
password = YOUR_PASSWORD
organization_id = 123456
```

- **app_token**: The app token for your custom Hubstaff-like API.  
- **email**, **password**: Credentials for retrieving `auth_token`.  
- **organization_id**: The numeric ID of your Hubstaff-like organization.  

The script automatically parses this file, so the sysadmin only needs to edit `config.ini` without touching the code.

---

## Cron Deployment

**Automate** daily HTML report generation using the **`deploy.sh`** script:

1. Make the script executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run it:
   ```bash
   ./deploy.sh
   ```
   - This script creates a virtual environment at `./env`, installs dependencies, and sets up a **cron job** that runs daily at **8:00 AM** (configurable in the script).
   - The cron output is redirected to either a **single file** (`daily_report.html` by default) or a **date-stamped file** (e.g., `daily_report_2025-04-14.html`) based on how you configure it.

3. **Confirm** the cron entry:
   ```bash
   crontab -l
   ```
   You should see a line similar to:
   ```bash
   0 8 * * * /path/to/hubstaff-daily-reports/env/bin/python /path/to/hubstaff-daily-reports/src/main.py > /path/to/daily_report.html
   ```
4. If you want to run it at a different time, edit `CRON_SCHEDULE` in `deploy.sh`.

---

## Running the Script Manually

If you’d like to run **ad hoc** rather than wait for cron:

```bash
# If not already active:
source env/bin/activate

# Generate the daily HTML report:
python src/main.py > daily_report.html
```

- **`daily_report.html`** will contain a table listing all the projects worked on and the users who logged time, along with total hours or minutes.

---

## Troubleshooting

1. **Empty HTML File**  
   - Verify that `report_day` matches a date where time was actually tracked.  
   - Ensure you have correct **app_token**, **email**, **password**, and **organization_id**.  
   - Check if the cron job **has actually run** yet or if you tested it manually.

2. **Authentication Failures**  
   - If `POST /v635/people/signin` fails, confirm you have valid credentials. The script logs to `stderr` upon errors (visible in your cron logs or terminal).

3. **macOS Permission Prompts**  
   - If your project lives in `~/Documents` or `~/Desktop`, macOS might prompt for access the first time it runs under cron. Either **grant Full Disk Access** to Python or move the project to a non-protected directory.

4. **Crontab Not Running**  
   - Make sure you’re using the **absolute path** to the Python executable in your `CRON_CMD`.  
   - If you’re on macOS, ensure that *root or your user’s crontab* is correct (`crontab -e`).  
   - Check logs: `grep CRON /var/log/syslog` (Linux) or `cat /tmp/cron.log` or `journalctl -u cron`.  

5. **Different Time Zones**  
   - The script uses UTC to compute “yesterday” by default. If you need a different time zone, you can modify the date logic in `config.py`.

---

## License

This project is licensed under the [Unlicense](LICENSE). You’re free to use, modify, and distribute it as you see fit.

---

**Enjoy your automated Hubstaff Daily Reports!** If you run into issues or have feature requests, please open an issue on GitHub or contact the maintainer.