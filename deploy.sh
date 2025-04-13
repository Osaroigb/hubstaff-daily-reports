#!/usr/bin/env bash
# This script automates the deployment of the hubstaff-daily-reports project.

# --------------- CONFIGURABLE VARIABLES ---------------
PROJECT_DIR=$(pwd)  # or specify an absolute path here
VENV_DIR="$PROJECT_DIR/env"
PYTHON_BIN="python3"
CRON_SCHEDULE="0 8 * * *"  # runs daily at 8:00 AM
# -----------------------------------------------------

echo "=== Deploying hubstaff-daily-reports ==="

# validate that config.ini is present
if [ ! -f "config.ini" ]; then
  echo "[ERROR] config.ini not found! Please create config.ini with your credentials."
  exit 1
fi

echo "config.ini found."

# Create/Activate Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR ..."
  $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Activate the venv
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install Python Dependencies
echo "Installing Python dependencies inside virtual environment..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# create a cron job that uses the venv Python
CRON_CMD="$VENV_DIR/bin/python $PROJECT_DIR/src/main.py > /var/www/html/daily_report_\$(date +\\%Y-\\%m-\\%d).html"

# remove any existing line from crontab that might conflict
crontab -l 2>/dev/null || true | grep -v "$CRON_CMD" > temp_cron

echo "$CRON_SCHEDULE $CRON_CMD" >> temp_cron
crontab temp_cron
rm temp_cron

echo "Cron job added: $CRON_SCHEDULE $CRON_CMD"
echo "Each day, a new HTML file will be generated in /var/www/html/ with today's date in its name."

echo "=== Deployment Complete ==="
echo "You can edit the cron schedule or path as needed in this script."