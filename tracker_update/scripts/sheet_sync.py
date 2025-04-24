# sheet_sync.py

import pandas as pd
import requests
import shutil
import os
import time
from io import StringIO
from datetime import datetime

def update_excel_sheet_from_google_sheet(download_url, excel_path, target_sheet_name, logger=None):
    start_time = time.time()
    job_name = f"{target_sheet_name} @ {os.path.basename(excel_path)}"

    try:
        # Step 1: Log start
        if logger:
            logger.info(f"Starting sync: {job_name}")

        # Step 2: Backup Excel file
        backup_path = create_excel_backup(excel_path)
        if logger:
            logger.info(f"Backup created: {backup_path}")

        # Step 3: Download sheet as CSV
        response = requests.get(download_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)

        # Step 4: Overwrite the target sheet
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=target_sheet_name, index=False)

        duration = time.time() - start_time
        if logger:
            logger.info(f"Sync completed: {job_name} (Time taken: {duration:.2f}s)")

    except Exception as e:
        if logger:
            logger.error(f"Sync failed: {job_name} | Error: {str(e)}")

def create_excel_backup(excel_path):
    base, ext = os.path.splitext(excel_path)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    backup_path = f"{base}_backup_{timestamp}{ext}"
    shutil.copy2(excel_path, backup_path)
    return backup_path
