import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

def export_to_excel_multisheet(results_dict, filename="output/all_output.xlsx"):
    try :
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            for sheet_name, df in results_dict.items():
                if not df.empty:
                    safe_name = sheet_name[:31]
                    df.to_excel(writer, sheet_name=safe_name, index=False)
    except Exception as e:
        logger.error(f"Failed to export results to Excel file {filename}: {e}")
        