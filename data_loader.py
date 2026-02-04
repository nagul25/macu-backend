"""
data_loader.py - Load and select rows from the Excel Data sheet.
"""

import pandas as pd
from io import BytesIO
from typing import List, Optional, Union


def load_data(xlsx_path: str, data_sheet: str = "Data") -> pd.DataFrame:
    """
    Load data from the Excel file's Data sheet.
    
    Args:
        xlsx_path: Path to the Excel file
        data_sheet: Name of the data sheet (default: "Data")
    
    Returns:
        DataFrame with the data
    """
    df = pd.read_excel(xlsx_path, sheet_name=data_sheet)
    return df


def load_data_from_bytes(
    excel_bytes: bytes,
    data_sheet: str = "Data"
) -> pd.DataFrame:
    """
    Load data from Excel bytes (for Azure Blob Storage integration).
    
    Args:
        excel_bytes: Excel file contents as bytes
        data_sheet: Name of the data sheet (default: "Data")
    
    Returns:
        DataFrame with the data
    
    Raises:
        ValueError: If sheet not found or data cannot be loaded
    """
    try:
        df = pd.read_excel(BytesIO(excel_bytes), sheet_name=data_sheet)
        return df
    except Exception as e:
        raise ValueError(f"Failed to load data from sheet '{data_sheet}': {e}")


def get_rows(
    df: pd.DataFrame,
    mode: str,
    row_index: Optional[int] = None,
    row_indices: Optional[List[int]] = None,
    start: int = 0,
    limit: int = 25
) -> pd.DataFrame:
    """
    Select rows from the DataFrame based on mode and parameters.
    
    Args:
        df: Source DataFrame
        mode: Either "single" or "batch"
        row_index: Index of single row (required for mode="single")
        row_indices: List of specific row indices (optional for mode="batch")
        start: Starting index for batch mode (default: 0)
        limit: Number of rows for batch mode (default: 25)
    
    Returns:
        DataFrame with selected rows (preserves original index)
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    max_index = len(df) - 1
    
    if mode == "single":
        if row_index is None:
            raise ValueError("row_index is required for single mode")
        
        if row_index < 0 or row_index > max_index:
            raise ValueError(
                f"row_index {row_index} is out of bounds. "
                f"Valid range: 0-{max_index}"
            )
        
        return df.iloc[[row_index]]
    
    elif mode == "batch":
        if row_indices is not None:
            # Use explicit list of indices
            valid_indices = []
            invalid_indices = []
            
            for idx in row_indices:
                if 0 <= idx <= max_index:
                    valid_indices.append(idx)
                else:
                    invalid_indices.append(idx)
            
            if invalid_indices:
                print(f"Warning: Skipping out-of-bounds indices: {invalid_indices}")
            
            if not valid_indices:
                raise ValueError("No valid row indices provided")
            
            return df.iloc[valid_indices]
        
        else:
            # Use start/limit
            if start < 0:
                raise ValueError(f"start must be >= 0, got {start}")
            
            if start > max_index:
                raise ValueError(
                    f"start {start} is out of bounds. "
                    f"Max index: {max_index}"
                )
            
            if limit <= 0:
                raise ValueError(f"limit must be > 0, got {limit}")
            
            end = min(start + limit, len(df))
            return df.iloc[start:end]
    
    else:
        raise ValueError(f"Invalid mode '{mode}'. Must be 'single' or 'batch'")


def parse_row_indices(indices_str: str) -> List[int]:
    """
    Parse a comma-separated string of row indices.
    
    Args:
        indices_str: String like "1,5,9" or "1, 5, 9"
    
    Returns:
        List of integers
    
    Raises:
        ValueError: If parsing fails
    """
    try:
        indices = [int(x.strip()) for x in indices_str.split(",")]
        return indices
    except ValueError as e:
        raise ValueError(f"Invalid row indices format '{indices_str}': {e}")


if __name__ == "__main__":
    # Quick test
    import sys
    
    xlsx_path = sys.argv[1] if len(sys.argv) > 1 else "Example Tags (1).xlsx"
    
    print(f"Loading data from {xlsx_path}...")
    df = load_data(xlsx_path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)[:10]}...")
    
    print("\n--- Testing single mode ---")
    single = get_rows(df, "single", row_index=5)
    print(f"Got {len(single)} row(s), index: {list(single.index)}")
    
    print("\n--- Testing batch mode (start/limit) ---")
    batch = get_rows(df, "batch", start=0, limit=5)
    print(f"Got {len(batch)} row(s), indices: {list(batch.index)}")
    
    print("\n--- Testing batch mode (explicit indices) ---")
    batch_explicit = get_rows(df, "batch", row_indices=[1, 5, 10])
    print(f"Got {len(batch_explicit)} row(s), indices: {list(batch_explicit.index)}")
    
    print("\n--- Testing parse_row_indices ---")
    print(f"'1,5,9' -> {parse_row_indices('1,5,9')}")
    print(f"'1, 5, 9' -> {parse_row_indices('1, 5, 9')}")

