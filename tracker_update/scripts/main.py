from config import SYNC_JOBS, MASTER_DB_CONFIG
from scripts.sheet_sync import update_excel_sheet_from_google_sheet
from scripts.masterdb_updater import process_master_db
from scripts.db_uploader import upload_to_postgres

import logging

# === Set up logging ===
logging.basicConfig(
    filename="sync_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_google_sheet_sync():
    logging.info("=== Sheet Sync Started ===")
    for job in SYNC_JOBS:
        update_excel_sheet_from_google_sheet(
            job["download_url"],
            job["excel_path"],
            job["target_sheet_name"],
            logger=logging
        )
    logging.info("=== Sheet Sync Finished ===\n")

def run_masterdb_sync():
    logging.info("=== MasterDB Sync Started ===")

    try:
        lte_csv, nr_csv = process_master_db(MASTER_DB_CONFIG)
    except Exception as e:
        logging.error(f" MasterDB extraction failed: {e}")
        return  # don’t proceed if extraction failed

    try:
        logging.info("Uploading LTE...")
        upload_to_postgres("lte", MASTER_DB_CONFIG["week_num"], lte_csv)
    except Exception as e:
        logging.error(f" LTE upload failed: {e}")

    try:
        logging.info("Uploading NR...")
        upload_to_postgres("nr", MASTER_DB_CONFIG["week_num"], nr_csv)
    except Exception as e:
        logging.error(f" NR upload failed: {e}")

    logging.info("=== MasterDB Sync Finished ===\n")


if __name__ == "__main__":
    run_google_sheet_sync()
    #run_masterdb_sync()
