#!/usr/bin/env python3
"""
run_poc.py - CLI entrypoint for the Excel tag classifier POC.

Usage:
    python run_poc.py single --row-index 10
    python run_poc.py batch --start 0 --limit 20
    python run_poc.py batch --row-indices 1,5,9 --out preds.csv
"""

import argparse
import sys
import time
import csv
from typing import List, Dict

from dotenv import load_dotenv

from taxonomy import load_taxonomy
from data_loader import load_data, get_rows, parse_row_indices
from classifier import get_azure_client, classify_summary


def truncate_text(text: str, max_len: int = 100) -> str:
    """Truncate text with ellipsis if too long."""
    if not text:
        return ""
    text = str(text).strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def print_result(
    row_index: int,
    case_summary: str,
    result: Dict,
    show_summary: bool = True,
    case_number: str = ""
) -> None:
    """Pretty print a classification result."""
    print(f"\n{'='*60}")
    print(f"Row Index: {row_index}")
    if case_number:
        print(f"Case Number: {case_number}")
    
    if show_summary:
        print(f"Summary: {truncate_text(case_summary, 150)}")
    
    print(f"\nPredicted Tags ({len(result['tags'])}):")
    if result['tags']:
        for i, (tag, classification) in enumerate(zip(result['tags'], result['classifications']), 1):
            print(f"  {i}. {tag}")
            if classification:
                print(f"     -> {classification}")
    else:
        print("  (none)")
    
    print(f"\nNeeds Review: {'YES' if result['needs_review'] else 'No'}")
    
    if result.get('error'):
        print(f"Error: {result['error']}")


def write_csv(results: List[Dict], output_path: str) -> None:
    """Write results to CSV file."""
    fieldnames = [
        'row_index',
        'case_number',
        'case_summary',
        'pred_tag_1', 'pred_tag_2', 'pred_tag_3', 'pred_tag_4',
        'actual_issue_1', 'actual_issue_2', 'actual_issue_3', 'actual_issue_4',
        'needs_review'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            tags = r['tags']
            row = {
                'row_index': r['row_index'],
                'case_number': r.get('case_number', ''),
                'case_summary': r.get('case_summary', ''),
                'pred_tag_1': tags[0] if len(tags) > 0 else '',
                'pred_tag_2': tags[1] if len(tags) > 1 else '',
                'pred_tag_3': tags[2] if len(tags) > 2 else '',
                'pred_tag_4': tags[3] if len(tags) > 3 else '',
                'actual_issue_1': r.get('actual_issue_1', ''),
                'actual_issue_2': r.get('actual_issue_2', ''),
                'actual_issue_3': r.get('actual_issue_3', ''),
                'actual_issue_4': r.get('actual_issue_4', ''),
                'needs_review': r['needs_review']
            }
            writer.writerow(row)
    
    print(f"\nResults written to: {output_path}")


def get_case_number(row) -> str:
    """Extract Case Number from a data row."""
    import pandas as pd
    value = row.get('Case Number', '')
    if value is None or pd.isna(value):
        return ''
    return str(value)


def get_actual_issues(row) -> Dict[str, str]:
    """Extract actual issue columns from a data row."""
    import pandas as pd
    actual_issues = {}
    for i in range(1, 5):
        col_name = f'Issue {i}'
        value = row.get(col_name, '')
        # Handle NaN values
        if value is None or pd.isna(value):
            value = ''
        actual_issues[f'actual_issue_{i}'] = str(value) if value else ''
    return actual_issues


def cmd_single(args) -> None:
    """Handle the 'single' subcommand."""
    print(f"Loading taxonomy from '{args.xlsx}' sheet '{args.tags_sheet}'...")
    allowed_tags, lower_to_tag, tag_to_class = load_taxonomy(
        args.xlsx, args.tags_sheet
    )
    allowed_set = set(allowed_tags)
    print(f"Loaded {len(allowed_tags)} allowed tags")
    
    print(f"\nLoading data from sheet '{args.data_sheet}'...")
    df = load_data(args.xlsx, args.data_sheet)
    print(f"Loaded {len(df)} rows")
    
    # Get the single row
    selected = get_rows(df, "single", row_index=args.row_index)
    row = selected.iloc[0]
    case_summary = row[args.summary_col]
    
    client, deployment = get_azure_client()
    
    print(f"\nClassifying row {args.row_index}...")
    result = classify_summary(
        client=client,
        deployment=deployment,
        case_summary=case_summary,
        allowed_tags=allowed_tags,
        allowed_set=allowed_set,
        lower_to_tag=lower_to_tag,
        tag_to_class=tag_to_class,
        top_k=args.top_k
    )
    
    case_number = get_case_number(row)
    print_result(args.row_index, case_summary, result, case_number=case_number)
    
    # Write CSV if requested
    if args.out:
        result['row_index'] = args.row_index
        result['case_number'] = case_number
        result['case_summary'] = str(case_summary) if case_summary else ''
        # Add actual issues from source data
        result.update(get_actual_issues(row))
        write_csv([result], args.out)


def cmd_batch(args) -> None:
    """Handle the 'batch' subcommand."""
    print(f"Loading taxonomy from '{args.xlsx}' sheet '{args.tags_sheet}'...")
    allowed_tags, lower_to_tag, tag_to_class = load_taxonomy(
        args.xlsx, args.tags_sheet
    )
    allowed_set = set(allowed_tags)
    print(f"Loaded {len(allowed_tags)} allowed tags")
    
    print(f"\nLoading data from sheet '{args.data_sheet}'...")
    df = load_data(args.xlsx, args.data_sheet)
    print(f"Loaded {len(df)} rows")
    
    # Determine row selection
    row_indices = None
    if args.row_indices:
        row_indices = parse_row_indices(args.row_indices)
        print(f"\nUsing explicit row indices: {row_indices}")
    else:
        print(f"\nUsing start={args.start}, limit={args.limit}")
    
    # Apply max_rows guard if set
    if args.max_rows and row_indices:
        if len(row_indices) > args.max_rows:
            print(f"Warning: Limiting to first {args.max_rows} rows (--max-rows)")
            row_indices = row_indices[:args.max_rows]
    elif args.max_rows and args.limit > args.max_rows:
        print(f"Warning: Limiting to {args.max_rows} rows (--max-rows)")
        args.limit = args.max_rows
    
    # Get selected rows
    selected = get_rows(
        df, "batch",
        row_indices=row_indices,
        start=args.start,
        limit=args.limit
    )
    
    print(f"Selected {len(selected)} rows for classification")
    
    client, deployment = get_azure_client()
    
    # Process each row
    results = []
    total = len(selected)
    
    print(f"\nClassifying {total} rows...")
    print("-" * 60)
    
    for i, (idx, row) in enumerate(selected.iterrows()):
        case_summary = row[args.summary_col]
        
        result = classify_summary(
            client=client,
            deployment=deployment,
            case_summary=case_summary,
            allowed_tags=allowed_tags,
            allowed_set=allowed_set,
            lower_to_tag=lower_to_tag,
            tag_to_class=tag_to_class,
            top_k=args.top_k
        )
        
        case_number = get_case_number(row)
        result['row_index'] = idx
        result['case_number'] = case_number
        result['case_summary'] = str(case_summary) if case_summary else ''
        # Add actual issues from source data
        result.update(get_actual_issues(row))
        results.append(result)
        
        print_result(idx, case_summary, result, case_number=case_number)
        
        # Progress indicator
        print(f"\n[Progress: {i+1}/{total}]")
        
        # Sleep between calls if specified
        if args.sleep_ms > 0 and i < total - 1:
            time.sleep(args.sleep_ms / 1000.0)
    
    # Summary
    print("\n" + "=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)
    print(f"Total rows processed: {total}")
    needs_review_count = sum(1 for r in results if r['needs_review'])
    print(f"Needs review: {needs_review_count}")
    print(f"Successfully classified: {total - needs_review_count}")
    
    # Write CSV if requested
    if args.out:
        write_csv(results, args.out)


def main() -> None:
    """Main CLI entrypoint."""
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description="Classify Excel case summaries into issue tags using Azure OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_poc.py single --row-index 10
    python run_poc.py batch --start 0 --limit 20
    python run_poc.py batch --row-indices 1,5,9 --out preds.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Common arguments for both subcommands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        '--xlsx',
        default='Example Tags (1).xlsx',
        help='Path to Excel file (default: Example Tags (1).xlsx)'
    )
    common.add_argument(
        '--data-sheet',
        default='Data',
        help='Name of data sheet (default: Data)'
    )
    common.add_argument(
        '--tags-sheet',
        default='Tags',
        help='Name of tags sheet (default: Tags)'
    )
    common.add_argument(
        '--summary-col',
        default='Case Summary',
        help='Name of case summary column (default: Case Summary)'
    )
    common.add_argument(
        '--top-k',
        type=int,
        default=4,
        help='Maximum number of tags to return (default: 4)'
    )
    common.add_argument(
        '--out',
        help='Output CSV path (optional)'
    )
    
    # Single subcommand
    single_parser = subparsers.add_parser(
        'single',
        parents=[common],
        help='Classify a single row'
    )
    single_parser.add_argument(
        '--row-index',
        type=int,
        required=True,
        help='Row index to classify (0-based)'
    )
    single_parser.set_defaults(func=cmd_single)
    
    # Batch subcommand
    batch_parser = subparsers.add_parser(
        'batch',
        parents=[common],
        help='Classify multiple rows'
    )
    batch_parser.add_argument(
        '--start',
        type=int,
        default=0,
        help='Starting row index (default: 0)'
    )
    batch_parser.add_argument(
        '--limit',
        type=int,
        default=25,
        help='Number of rows to process (default: 25)'
    )
    batch_parser.add_argument(
        '--row-indices',
        help='Comma-separated list of row indices (overrides start/limit)'
    )
    batch_parser.add_argument(
        '--sleep-ms',
        type=int,
        default=0,
        help='Sleep between API calls in milliseconds (default: 0)'
    )
    batch_parser.add_argument(
        '--max-rows',
        type=int,
        default=None,
        help='Maximum rows to process (guard against large runs)'
    )
    batch_parser.set_defaults(func=cmd_batch)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

