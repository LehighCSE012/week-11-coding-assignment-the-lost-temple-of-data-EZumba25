import re  # Standard library import
import pandas as pd  # Third-party import

def load_artifact_data(excel_filepath):
    """
    Reads artifact data from a specific sheet ('Main Chamber') in an Excel file,
    skipping the first 3 rows.

    Args:
        excel_filepath (str): The path to the artifacts Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the artifact data.
    """
    try:
        # Read the Excel file, skip the first 3 rows, and load the 'Main Chamber' sheet
        df = pd.read_excel(excel_filepath, sheet_name='Main Chamber', skiprows=3)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {excel_filepath}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {excel_filepath} is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def load_location_notes(tsv_filepath):
    """
    Reads location data from a Tab-Separated Value (TSV) file.

    Args:
        tsv_filepath (str): The path to the locations TSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the location data.
    """
    try:
        # Read the TSV file, specifying '\t' as the separator
        df = pd.read_csv(tsv_filepath, sep='\t')
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {tsv_filepath}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {tsv_filepath} is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def extract_journal_dates(journal_text):
    """
    Extracts all dates in MM/DD/YYYY format from the journal text.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of date strings found in the text.
    """
    # Regular expression to match dates in MM/DD/YYYY format
    date_pattern = r"\d{2}/\d{2}/\d{4}"
    dates = re.findall(date_pattern, journal_text)
    return dates

def extract_secret_codes(journal_text):
    """
    Extracts all secret codes in AZMAR-XXX format (XXX are digits) from the journal text.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of secret code strings found in the text.
    """
    # Regular expression to match AZMAR- followed by 3 digits
    code_pattern = r"AZMAR-\d{3}"
    codes = re.findall(code_pattern, journal_text)
    return codes


# --- Optional: Main execution block for your own testing ---
if __name__ == '__main__':
    # Define file paths (adjust if your files are located elsewhere)
    EXCEL_FILE = 'artifacts.xlsx'
    TSV_FILE = 'locations.tsv'
    JOURNAL_FILE = 'journal.txt'

    print(f"--- Loading Artifact Data from {EXCEL_FILE} ---")
    try:
        artifacts_df = load_artifact_data(EXCEL_FILE)
        if artifacts_df is not None:
            print("Successfully loaded DataFrame. First 5 rows:")
            print(artifacts_df.head())
            print("\nDataFrame Info:")
            artifacts_df.info()
    except Exception as e:
        print(f"An error occurred loading artifact data: {e}")

    print(f"\n--- Loading Location Notes from {TSV_FILE} ---")
    try:
        locations_df = load_location_notes(TSV_FILE)
        if locations_df is not None:
            print("Successfully loaded DataFrame. First 5 rows:")
            print(locations_df.head())
            print("\nDataFrame Info:")
            locations_df.info()
    except Exception as e:
        print(f"An error occurred loading location data: {e}")

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
    except Exception as e:
        print(f"An unexpected error occurred processing the journal: {e}")
