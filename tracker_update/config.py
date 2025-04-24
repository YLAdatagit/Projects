# config.py

SYNC_JOBS = [
    {
        "download_url": "https://docs.google.com/spreadsheets/d/118XNSrCAwANVyUhHSzP2v7ERAsETPRSM/export?format=csv&gid=250048890#gid=250048890",
        "excel_path": r"D:\D&T Project\Progress\CCS Progress tracker_Update.xlsx",
        "target_sheet_name": "RAW",
    },
    {
        "download_url": "https://docs.google.com/spreadsheets/d/118XNSrCAwANVyUhHSzP2v7ERAsETPRSM/export?format=csv&gid=1436606241#gid=1436606241&fvid=655906441",
        "excel_path": r"D:\D&T Project\Progress\CCS Progress tracker_Update.xlsx",
        "target_sheet_name": "Cluster Progress",
    }
]

MASTER_DB_CONFIG = {
    "rar_base_path": r"D:\D&T Project\Database\Master DB",
    "week_num": "WK2515",  # 👈 optional: could auto-detect from filename later
    "excel_filename_pattern": "MasterDB updated process_BMA_{week_num}.xlsx",
    "rar_filename_pattern": "MasterDB updated process_BMA_{week_num}.rar",
    "sheets_to_extract": {
        "LTE": "MD_LTE_{week_num}.csv",
        "NR": "MD_NR_{week_num}.csv"
    },
    "output_folder": r"D:\D&T Project\Database\Master DB\Processed"
}