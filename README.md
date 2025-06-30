# Repository Overview

This repository collects various scripts and notebooks used for processing network data and synchronizing progress trackers.  Each folder represents a separate task or workflow.  The projects are independent and may require custom configurations depending on your environment.

## Folders

- **CR_Checking** – Contains `parse_mml_results.py`, a Tkinter GUI that parses MML command results from a text file and saves them as CSV.
- **dump_file_data_processing** – Pipeline for unpacking RAR archives, shifting and converting CSV/Excel data, and uploading tilt values to PostgreSQL.  See `scripts/main.py` and `config.py` for configuration options.
- **tracker_update** – Utilities for keeping progress trackers in sync.  `scripts/main.py` downloads Google Sheets data into an Excel workbook, processes MasterDB updates, and uploads weekly data to PostgreSQL.
- **Daily ipynb files** – Assorted Jupyter notebooks for daily reporting tasks.  Currently includes `CR_generating_V2.ipynb`.
- **Plannar** – Notebook (`Plannar_zip.ipynb`) with planning or analysis routines.

## Requirements

The scripts assume Python 3 and rely on common packages such as `pandas`, `openpyxl`, `psycopg2`, and `rarfile`.  Some workflows require WinRAR for extraction and network/database access configured in the corresponding `config.py` files.

## Usage

Most folders can be run independently.  Review the `config.py` or notebook instructions inside each directory, install the required dependencies, and execute the main script or notebook that suits your task.  The repository has no unified entry point or package structure.

