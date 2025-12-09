"""
taxonomy.py - Load and process allowed tags from the Excel Tags sheet.
"""

import pandas as pd
from typing import Tuple, Dict, List


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
    
    return allowed_tags, lower_to_tag, tag_to_class


if __name__ == "__main__":
    # Quick test
    import sys
    
    xlsx_path = sys.argv[1] if len(sys.argv) > 1 else "Example Tags (1).xlsx"
    
    allowed_tags, lower_to_tag, tag_to_class = load_taxonomy(xlsx_path)
    
    print(f"Loaded {len(allowed_tags)} unique tags")
    print("\nFirst 5 tags with classifications:")
    for tag in allowed_tags[:5]:
        print(f"  - {tag} -> {tag_to_class.get(tag, 'N/A')}")

