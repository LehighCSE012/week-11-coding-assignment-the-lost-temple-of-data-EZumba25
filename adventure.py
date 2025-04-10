import re
from datetime import datetime
import pandas as pd


def load_artifact_data(excel_filepath):
    """
    Reads artifact data from a specific sheet ('Main Chamber') in an Excel file,
    skipping the first 3 rows.

    Args:
        excel_filepath (str): The path to the artifacts Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the artifact data or None if error.
    """
    try:
        df = pd.read_excel(excel_filepath, sheet_name='Main Chamber', skiprows=3)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {excel_filepath}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {excel_filepath} is empty.")
    except IOError as e:
        print(f"Error: I/O error occurred while accessing {excel_filepath}: {e}")
    return None


def load_location_notes(tsv_filepath):
    """
    Reads location data from a Tab-Separated Value (TSV) file.

    Args:
        tsv_filepath (str): The path to the locations TSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the location data or None if error.
    """
    try:
        df = pd.read_csv(tsv_filepath, sep='\t')
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {tsv_filepath}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {tsv_filepath} is empty.")
    except IOError as e:
        print(f"Error: I/O error occurred while accessing {tsv_filepath}: {e}")
    return None


def extract_journal_dates(journal_text):
    """
    Extracts all dates in MM/DD/YYYY format from the journal text and validates them.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of valid date strings found in the text.
    """
    date_pattern = r"\d{2}/\d{2}/\d{4}"
    dates = re.findall(date_pattern, journal_text)

    valid_dates = []
    for date in dates:
        try:
            parsed_date = datetime.strptime(date, "%m/%d/%Y")
            if 1 <= parsed_date.month <= 12 and 1 <= parsed_date.day <= 31:
                valid_dates.append(date)
        except ValueError:
            continue

    return valid_dates


def extract_secret_codes(journal_text):
    """
    Extracts all secret codes in AZMAR-XXX format (XXX are digits) from the journal text.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of secret code strings found in the text.
    """
    code_pattern = r"AZMAR-\d{3}"
    codes = re.findall(code_pattern, journal_text)
    return codes


# --- Optional: Main execution block for your own testing ---
if __name__ == '__main__':
    EXCEL_FILE = 'artifacts.xlsx'
    TSV_FILE = 'locations.tsv'
    JOURNAL_FILE = 'journal.txt'

    print(f"--- Loading Artifact Data from {EXCEL_FILE} ---")
    artifacts_df = load_artifact_data(EXCEL_FILE)
    if artifacts_df is not None:
        print("Successfully loaded DataFrame. First 5 rows:")
        print(artifacts_df.head())
        print("\nDataFrame Info:")
        artifacts_df.info()

    print(f"\n--- Loading Location Notes from {TSV_FILE} ---")
    locations_df = load_location_notes(TSV_FILE)
    if locations_df is not None:
        print("Successfully loaded DataFrame. First 5 rows:")
        print(locations_df.head())
        print("\nDataFrame Info:")
        locations_df.info()

    print(f"\n--- Processing Journal from {JOURNAL_FILE} ---")
    try:
        with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
            journal_content = f.read()

        print("\nExtracting Dates...")
        extracted_dates = extract_journal_dates(journal_content)
        print(f"Found dates: {extracted_dates}")

        print("\nExtracting Secret Codes...")
        extracted_codes = extract_secret_codes(journal_content)
        print(f"Found codes: {extracted_codes}")

    except FileNotFoundError:
        print(f"Error: File not found at {JOURNAL_FILE}")
