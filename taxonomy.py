"""
taxonomy.py - Load and process allowed tags from the Excel Tags sheet.
"""

import pandas as pd
from io import BytesIO
from typing import Tuple, Dict, List, Union


# Additional tags identified from feedback that may not be in the Excel file yet
# These will be added to the allowed tags list
SUPPLEMENTAL_TAGS = {
    "account charge off": "Account Management",
    "garnishment": "Account Management",
    "adjustment": "Transaction Issues",
    "rep payee": "Account Management",
}


def _process_taxonomy_df(
    df: pd.DataFrame,
    tags_sheet: str,
    issues_col: str,
    classification_col: str
) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """
    Process a taxonomy DataFrame into the required data structures.
    
    Internal helper function used by both load_taxonomy and load_taxonomy_from_bytes.
    """
    # Validate required columns exist
    if issues_col not in df.columns:
        raise ValueError(f"Column '{issues_col}' not found in sheet '{tags_sheet}'")
    if classification_col not in df.columns:
        raise ValueError(f"Column '{classification_col}' not found in sheet '{tags_sheet}'")
    
    # Build data structures
    allowed_tags: List[str] = []
    lower_to_tag: Dict[str, str] = {}
    tag_to_class: Dict[str, str] = {}
    
    seen_lower: set = set()
    
    for _, row in df.iterrows():
        tag = row[issues_col]
        classification = row[classification_col]
        
        # Skip NaN values
        if pd.isna(tag):
            continue
            
        tag_str = str(tag).strip()
        tag_lower = tag_str.lower()
        
        # Deduplicate while preserving order
        if tag_lower not in seen_lower:
            seen_lower.add(tag_lower)
            allowed_tags.append(tag_str)
            lower_to_tag[tag_lower] = tag_str
            
            # Map tag to classification (handle NaN classification)
            if pd.notna(classification):
                tag_to_class[tag_str] = str(classification).strip()
            else:
                tag_to_class[tag_str] = ""
    
    # Add supplemental tags that may not be in the Excel file yet
    for tag, classification in SUPPLEMENTAL_TAGS.items():
        tag_lower = tag.lower()
        if tag_lower not in seen_lower:
            seen_lower.add(tag_lower)
            allowed_tags.append(tag)
            lower_to_tag[tag_lower] = tag
            tag_to_class[tag] = classification
    
    return allowed_tags, lower_to_tag, tag_to_class


def load_taxonomy(
    xlsx_path: str,
    tags_sheet: str = "Tags",
    issues_col: str = "Issues",
    classification_col: str = "Classification"
) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """
    Load the taxonomy of allowed tags from the Excel file.
    
    Args:
        xlsx_path: Path to the Excel file
        tags_sheet: Name of the sheet containing tags (default: "Tags")
        issues_col: Column name for issue tags (default: "Issues")
        classification_col: Column name for classifications (default: "Classification")
    
    Returns:
        Tuple of:
            - allowed_tags: List of unique tag strings (preserves original order)
            - lower_to_tag: Dict mapping lowercase tag to original case
            - tag_to_class: Dict mapping tag to its classification
    """
    # Read the tags sheet
    df = pd.read_excel(xlsx_path, sheet_name=tags_sheet)
    return _process_taxonomy_df(df, tags_sheet, issues_col, classification_col)


def load_taxonomy_from_bytes(
    excel_bytes: bytes,
    tags_sheet: str = "Tags",
    issues_col: str = "Issues",
    classification_col: str = "Classification"
) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """
    Load the taxonomy of allowed tags from Excel bytes (for Azure Blob Storage integration).
    
    Args:
        excel_bytes: Excel file contents as bytes
        tags_sheet: Name of the sheet containing tags (default: "Tags")
        issues_col: Column name for issue tags (default: "Issues")
        classification_col: Column name for classifications (default: "Classification")
    
    Returns:
        Tuple of:
            - allowed_tags: List of unique tag strings (preserves original order)
            - lower_to_tag: Dict mapping lowercase tag to original case
            - tag_to_class: Dict mapping tag to its classification
    
    Raises:
        ValueError: If sheet not found or taxonomy cannot be loaded
    """
    try:
        df = pd.read_excel(BytesIO(excel_bytes), sheet_name=tags_sheet)
        return _process_taxonomy_df(df, tags_sheet, issues_col, classification_col)
    except ValueError:
        # Re-raise ValueError from _process_taxonomy_df
        raise
    except Exception as e:
        raise ValueError(f"Failed to load taxonomy from sheet '{tags_sheet}': {e}")


if __name__ == "__main__":
    # Quick test
    import sys
    
    xlsx_path = sys.argv[1] if len(sys.argv) > 1 else "Example Tags (1).xlsx"
    
    allowed_tags, lower_to_tag, tag_to_class = load_taxonomy(xlsx_path)
    
    print(f"Loaded {len(allowed_tags)} unique tags")
    print("\nFirst 5 tags with classifications:")
    for tag in allowed_tags[:5]:
        print(f"  - {tag} -> {tag_to_class.get(tag, 'N/A')}")

