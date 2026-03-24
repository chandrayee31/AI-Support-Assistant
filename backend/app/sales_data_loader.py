from pathlib import Path
import pandas as pd
from app.file_state import get_active_file
from typing import Optional

UPLOAD_DIR = Path(__file__).parent / "uploaded_files"


def list_uploaded_sales_files():
    files = list(UPLOAD_DIR.glob("*.csv")) + list(UPLOAD_DIR.glob("*.xlsx"))
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def get_latest_uploaded_sales_file():
    files = list_uploaded_sales_files()
    return files[0] if files else None


def get_sales_file_by_name(filename: str):
    if not filename:
        return None

    candidate = UPLOAD_DIR / filename
    if candidate.exists() and candidate.is_file():
        return candidate

    return None



def load_sales_data(filename: Optional[str] = None):
    """
    Load a specific uploaded sales file if filename is provided.
    Otherwise, load the latest uploaded file.
    Supports CSV/XLSX and tries multiple CSV encodings.
    """
    target_file = get_sales_file_by_name(filename) if filename else get_latest_uploaded_sales_file()

    if target_file is None:
        return None, "No uploaded sales file found."

    try:
        suffix = target_file.suffix.lower()

        if suffix == ".xlsx":
            df = pd.read_excel(target_file)
            return df, None

        if suffix == ".csv":
            encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin1"]

            last_error = None
            for enc in encodings_to_try:
                try:
                    df = pd.read_csv(target_file, encoding=enc)
                    return df, None
                except Exception as e:
                    last_error = e

            return None, f"Failed to load CSV with supported encodings: {str(last_error)}"

        return None, "Unsupported file type."

    except Exception as e:
        return None, f"Failed to load sales file: {str(e)}"


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        col.strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    ]
    return df


def load_sales_data(filename: Optional[str] = None):
    """
    Load a specific uploaded sales file if filename is provided.
    Otherwise, use active file if set.
    Otherwise, load the latest uploaded file.
    """
    chosen_filename = filename or get_active_file()
    target_file = get_sales_file_by_name(chosen_filename) if chosen_filename else get_latest_uploaded_sales_file()

    if target_file is None:
        return None, "No uploaded sales file found."

    try:
        suffix = target_file.suffix.lower()

        if suffix == ".xlsx":
            df = pd.read_excel(target_file)
            return df, None

        if suffix == ".csv":
            encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin1"]

            last_error = None
            for enc in encodings_to_try:
                try:
                    df = pd.read_csv(target_file, encoding=enc)
                    return df, None
                except Exception as e:
                    last_error = e

            return None, f"Failed to load CSV with supported encodings: {str(last_error)}"

        return None, "Unsupported file type."

    except Exception as e:
        return None, f"Failed to load sales file: {str(e)}"