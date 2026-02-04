#!/usr/bin/env python3
"""
run_blob_processor.py - Process Excel files from Azure Blob Storage.

This script reads Excel files from an Azure Blob Storage input folder,
classifies them using the tag classifier model, and stores results
in an output folder. Failed files are moved to a review folder.

Usage:
    # Process all files in input folder once
    python run_blob_processor.py process --container mycontainer

    # Continuously watch for new files
    python run_blob_processor.py watch --container mycontainer --interval 60

    # Process with custom folders
    python run_blob_processor.py process --container mycontainer --input-folder incoming --output-folder results
"""

import argparse
import os
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import pandas as pd
from dotenv import load_dotenv

from blob_storage import (
    list_input_blobs,
    download_blob_to_bytes,
    upload_blob,
    move_to_archive,
    move_to_review,
    ensure_folders_exist,
)
from classifier import get_azure_client, classify_summary
from data_loader import load_data_from_bytes
from taxonomy import load_taxonomy_from_bytes
from logging_config import setup_logging, get_file_logger, log_system


def process_single_file(
    container_name: str,
    blob_name: str,
    excel_bytes: bytes,
    data_sheet: str = "Data",
    tags_sheet: str = "Tags",
    summary_col: str = "Case Summary",
    top_k: int = 4,
    sleep_ms: int = 0
) -> Tuple[pd.DataFrame, Dict]:
    """
    Process a single Excel file through the classifier.
    
    Args:
        container_name: Azure Blob Storage container name
        blob_name: Full path to the blob
        excel_bytes: Excel file contents as bytes
        data_sheet: Name of the data sheet
        tags_sheet: Name of the tags sheet
        summary_col: Name of the case summary column
        top_k: Maximum number of tags per row
        sleep_ms: Sleep between API calls in milliseconds
    
    Returns:
        Tuple of (results_dataframe, summary_dict)
    
    Raises:
        Exception: If processing fails at any stage
    """
    filename = os.path.basename(blob_name)
    file_logger = get_file_logger(filename)
    
    # Load taxonomy
    file_logger.info("taxonomy", f"Loading taxonomy from '{tags_sheet}' sheet")
    allowed_tags, lower_to_tag, tag_to_class = load_taxonomy_from_bytes(
        excel_bytes, tags_sheet
    )
    allowed_set = set(allowed_tags)
    file_logger.info("taxonomy", f"Loaded {len(allowed_tags)} allowed tags")
    
    # Load data
    file_logger.info("data", f"Loading data from '{data_sheet}' sheet")
    df = load_data_from_bytes(excel_bytes, data_sheet)
    total_rows = len(df)
    file_logger.info("data", f"Loaded {total_rows} rows for classification")
    
    # Get Azure OpenAI client
    file_logger.info("classify", "Connecting to Azure OpenAI")
    client, deployment = get_azure_client()
    
    # Process each row
    file_logger.info("classify", f"Starting classification ({total_rows} rows)")
    
    results = []
    needs_review_count = 0
    error_count = 0
    
    for row_num, (idx, row) in enumerate(df.iterrows(), 1):
        case_summary = row.get(summary_col, "")
        
        file_logger.info("classify", f"Processing row {row_num}/{total_rows}", row=idx)
        
        try:
            result = classify_summary(
                client=client,
                deployment=deployment,
                case_summary=case_summary,
                allowed_tags=allowed_tags,
                allowed_set=allowed_set,
                lower_to_tag=lower_to_tag,
                tag_to_class=tag_to_class,
                top_k=top_k
            )
            
            # Log the assigned tags
            tags_str = ", ".join(result["tags"]) if result["tags"] else "(none)"
            file_logger.info("classify", f"Row {row_num}/{total_rows} -> {tags_str}", row=idx)
            
            if result.get("needs_review"):
                needs_review_count += 1
            
            if result.get("error"):
                error_count += 1
                file_logger.warning(
                    "classify",
                    f"Row {idx} classification had error: {result.get('error')}",
                    row=idx
                )
            
        except Exception as e:
            file_logger.warning("classify", f"Row {idx} failed: {e}", row=idx, exc_info=False)
            result = {
                "tags": [],
                "classifications": [],
                "needs_review": True,
                "error": str(e)
            }
            needs_review_count += 1
            error_count += 1
        
        # Build result row
        result_row = {
            "row_index": idx,
            "case_summary": str(case_summary) if case_summary else "",
            "pred_tag_1": result["tags"][0] if len(result["tags"]) > 0 else "",
            "pred_tag_2": result["tags"][1] if len(result["tags"]) > 1 else "",
            "pred_tag_3": result["tags"][2] if len(result["tags"]) > 2 else "",
            "pred_tag_4": result["tags"][3] if len(result["tags"]) > 3 else "",
            "pred_class_1": result["classifications"][0] if len(result["classifications"]) > 0 else "",
            "pred_class_2": result["classifications"][1] if len(result["classifications"]) > 1 else "",
            "pred_class_3": result["classifications"][2] if len(result["classifications"]) > 2 else "",
            "pred_class_4": result["classifications"][3] if len(result["classifications"]) > 3 else "",
            "needs_review": result["needs_review"],
            "error": result.get("error", "")
        }
        
        # Add original issue columns if present
        for i in range(1, 5):
            col_name = f"Issue {i}"
            if col_name in row:
                value = row[col_name]
                if pd.isna(value):
                    value = ""
                result_row[f"actual_issue_{i}"] = str(value) if value else ""
        
        results.append(result_row)
        
        # Sleep between API calls if specified
        if sleep_ms > 0 and idx < total_rows - 1:
            time.sleep(sleep_ms / 1000.0)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    summary = {
        "total_rows": total_rows,
        "needs_review_count": needs_review_count,
        "error_count": error_count,
        "success_count": total_rows - needs_review_count
    }
    
    file_logger.info(
        "classify",
        f"Classification complete ({total_rows}/{total_rows} rows, "
        f"{needs_review_count} need review, {error_count} errors)"
    )
    
    return results_df, summary


def save_results_to_blob(
    container_name: str,
    results_df: pd.DataFrame,
    original_filename: str,
    output_folder: str = "output"
) -> Tuple[str, str]:
    """
    Save results to blob storage as both Excel and CSV.
    
    Args:
        container_name: Azure Blob Storage container name
        results_df: DataFrame with results
        original_filename: Original input filename (used to derive output name)
        output_folder: Output folder name
    
    Returns:
        Tuple of (excel_blob_path, csv_blob_path)
    """
    file_logger = get_file_logger(original_filename)
    
    # Generate output filenames
    base_name = os.path.splitext(original_filename)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_name = f"{base_name}_predictions_{timestamp}.xlsx"
    csv_name = f"{base_name}_predictions_{timestamp}.csv"
    
    excel_path = f"{output_folder}/{excel_name}"
    csv_path = f"{output_folder}/{csv_name}"
    
    file_logger.info("upload", f"Uploading predictions to {output_folder}/")
    
    # Save Excel
    excel_buffer = BytesIO()
    results_df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_bytes = excel_buffer.getvalue()
    upload_blob(container_name, excel_path, excel_bytes)
    
    excel_size_kb = len(excel_bytes) / 1024
    file_logger.info("upload", f"Uploaded {excel_name} ({excel_size_kb:.1f} KB)")
    
    # Save CSV
    csv_buffer = BytesIO()
    results_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue()
    upload_blob(container_name, csv_path, csv_bytes)
    
    csv_size_kb = len(csv_bytes) / 1024
    file_logger.info("upload", f"Uploaded {csv_name} ({csv_size_kb:.1f} KB)")
    
    return excel_path, csv_path


def process_blob(
    container_name: str,
    blob_name: str,
    input_folder: str = "input",
    output_folder: str = "output",
    archive_folder: str = "archive",
    review_folder: str = "review",
    data_sheet: str = "Data",
    tags_sheet: str = "Tags",
    summary_col: str = "Case Summary",
    top_k: int = 4,
    sleep_ms: int = 0
) -> bool:
    """
    Process a single blob end-to-end with error handling.
    
    Downloads the file, processes it, uploads results, and moves the original
    to archive (on success) or review (on failure).
    
    Args:
        container_name: Azure Blob Storage container name
        blob_name: Full path to the input blob
        input_folder: Input folder name
        output_folder: Output folder name
        archive_folder: Archive folder name
        review_folder: Review folder name
        data_sheet: Name of the data sheet
        tags_sheet: Name of the tags sheet
        summary_col: Name of the case summary column
        top_k: Maximum number of tags per row
        sleep_ms: Sleep between API calls in milliseconds
    
    Returns:
        True if processing succeeded, False if file was moved to review
    """
    filename = os.path.basename(blob_name)
    file_logger = get_file_logger(filename)
    
    file_logger.info("start", f"Starting processing of {blob_name}")
    start_time = time.time()
    
    try:
        # Download the file
        excel_bytes, size_bytes = download_blob_to_bytes(container_name, blob_name)
        
        # Process the file
        results_df, summary = process_single_file(
            container_name=container_name,
            blob_name=blob_name,
            excel_bytes=excel_bytes,
            data_sheet=data_sheet,
            tags_sheet=tags_sheet,
            summary_col=summary_col,
            top_k=top_k,
            sleep_ms=sleep_ms
        )
        
        # Save results
        excel_path, csv_path = save_results_to_blob(
            container_name=container_name,
            results_df=results_df,
            original_filename=filename,
            output_folder=output_folder
        )
        
        # Move original to archive
        move_to_archive(container_name, blob_name, archive_folder)
        
        elapsed = time.time() - start_time
        file_logger.info(
            "complete",
            f"Processing completed successfully in {elapsed:.1f}s "
            f"(rows: {summary['total_rows']}, needs_review: {summary['needs_review_count']})"
        )
        
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        
        # Log the full error with traceback
        file_logger.error(
            "error",
            f"Processing failed after {elapsed:.1f}s: {e}"
        )
        
        # Log the full traceback
        tb = traceback.format_exc()
        file_logger.error("error", f"Traceback:\n{tb}", exc_info=False)
        
        # Move to review folder
        try:
            move_to_review(container_name, blob_name, review_folder)
        except Exception as move_error:
            file_logger.error(
                "review",
                f"Failed to move file to review folder: {move_error}"
            )
        
        return False


def cmd_process(args) -> None:
    """Handle the 'process' subcommand - one-time processing of all input files."""
    log_system("startup", "Blob processor starting in PROCESS mode")
    log_system("config", f"Container: {args.container}, Input: {args.input_folder}")
    
    # Ensure all required folders exist (creates .keep placeholders)
    ensure_folders_exist(
        container_name=args.container,
        folders=[args.input_folder, args.output_folder, args.archive_folder, args.review_folder]
    )
    
    # List files in input folder
    log_system("list", f"Scanning for Excel files in {args.input_folder}/")
    blobs = list_input_blobs(
        container_name=args.container,
        input_folder=args.input_folder,
        file_extension=".xlsx"
    )
    
    if not blobs:
        log_system("list", "No Excel files found in input folder")
        print("No files to process.")
        return
    
    log_system("list", f"Found {len(blobs)} file(s) to process")
    
    # Process each file
    success_count = 0
    failure_count = 0
    
    for i, blob_name in enumerate(blobs, 1):
        log_system("progress", f"Processing file {i}/{len(blobs)}: {blob_name}")
        
        success = process_blob(
            container_name=args.container,
            blob_name=blob_name,
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            archive_folder=args.archive_folder,
            review_folder=args.review_folder,
            data_sheet=args.data_sheet,
            tags_sheet=args.tags_sheet,
            summary_col=args.summary_col,
            top_k=args.top_k,
            sleep_ms=args.sleep_ms
        )
        
        if success:
            success_count += 1
        else:
            failure_count += 1
    
    # Summary
    log_system(
        "summary",
        f"Processing complete. Success: {success_count}, Failed: {failure_count}"
    )
    print(f"\nProcessing complete:")
    print(f"  Successful: {success_count}")
    print(f"  Failed (moved to review): {failure_count}")


def cmd_watch(args) -> None:
    """Handle the 'watch' subcommand - continuous polling for new files."""
    log_system("startup", "Blob processor starting in WATCH mode")
    log_system(
        "config",
        f"Container: {args.container}, Input: {args.input_folder}, "
        f"Interval: {args.interval}s"
    )
    
    # Ensure all required folders exist (creates .keep placeholders)
    ensure_folders_exist(
        container_name=args.container,
        folders=[args.input_folder, args.output_folder, args.archive_folder, args.review_folder]
    )
    
    print(f"Watching {args.container}/{args.input_folder}/ for new files...")
    print(f"Poll interval: {args.interval} seconds")
    print("Press Ctrl+C to stop.\n")
    
    total_processed = 0
    total_failed = 0
    
    try:
        while True:
            # List files in input folder
            try:
                blobs = list_input_blobs(
                    container_name=args.container,
                    input_folder=args.input_folder,
                    file_extension=".xlsx"
                )
            except Exception as e:
                log_system("error", f"Failed to list blobs: {e}", level="ERROR")
                time.sleep(args.interval)
                continue
            
            if blobs:
                log_system("watch", f"Found {len(blobs)} file(s) to process")
                
                for blob_name in blobs:
                    success = process_blob(
                        container_name=args.container,
                        blob_name=blob_name,
                        input_folder=args.input_folder,
                        output_folder=args.output_folder,
                        archive_folder=args.archive_folder,
                        review_folder=args.review_folder,
                        data_sheet=args.data_sheet,
                        tags_sheet=args.tags_sheet,
                        summary_col=args.summary_col,
                        top_k=args.top_k,
                        sleep_ms=args.sleep_ms
                    )
                    
                    if success:
                        total_processed += 1
                    else:
                        total_failed += 1
                
                log_system(
                    "watch",
                    f"Batch complete. Total processed: {total_processed}, "
                    f"Total failed: {total_failed}"
                )
            
            # Wait before next poll
            log_system("watch", f"Waiting {args.interval}s before next poll...", level="DEBUG")
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        log_system("shutdown", "Watch mode stopped by user")
        print(f"\n\nWatch mode stopped.")
        print(f"Total processed: {total_processed}")
        print(f"Total failed: {total_failed}")


def main() -> None:
    """Main CLI entrypoint."""
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description="Process Excel files from Azure Blob Storage through the tag classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_blob_processor.py process --container mycontainer
    python run_blob_processor.py watch --container mycontainer --interval 60
    python run_blob_processor.py process --container mycontainer --log-level DEBUG
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Common arguments
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        '--container',
        default=os.environ.get('AZURE_BLOB_CONTAINER'),
        help='Azure Blob Storage container name (or set AZURE_BLOB_CONTAINER env var)'
    )
    common.add_argument(
        '--input-folder',
        default='input',
        help='Input folder name in container (default: input)'
    )
    common.add_argument(
        '--output-folder',
        default='output',
        help='Output folder name in container (default: output)'
    )
    common.add_argument(
        '--archive-folder',
        default='archive',
        help='Archive folder name for processed files (default: archive)'
    )
    common.add_argument(
        '--review-folder',
        default='review',
        help='Review folder name for failed files (default: review)'
    )
    common.add_argument(
        '--data-sheet',
        default='Data',
        help='Name of data sheet in Excel files (default: Data)'
    )
    common.add_argument(
        '--tags-sheet',
        default='Tags',
        help='Name of tags sheet in Excel files (default: Tags)'
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
        help='Maximum number of tags per row (default: 4)'
    )
    common.add_argument(
        '--sleep-ms',
        type=int,
        default=0,
        help='Sleep between API calls in milliseconds (default: 0)'
    )
    common.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Log level (default: INFO)'
    )
    common.add_argument(
        '--log-file',
        default=None,
        help='Custom log file path (default: logs/processor_YYYYMMDD.log)'
    )
    
    # Process subcommand
    process_parser = subparsers.add_parser(
        'process',
        parents=[common],
        help='Process all files in input folder once'
    )
    process_parser.set_defaults(func=cmd_process)
    
    # Watch subcommand
    watch_parser = subparsers.add_parser(
        'watch',
        parents=[common],
        help='Continuously watch for and process new files'
    )
    watch_parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Polling interval in seconds (default: 60)'
    )
    watch_parser.set_defaults(func=cmd_watch)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Validate container
    if not args.container:
        print("Error: Container name is required. Use --container or set AZURE_BLOB_CONTAINER env var.")
        sys.exit(1)
    
    # Setup logging
    setup_logging(log_file=args.log_file, level=args.log_level)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        log_system("shutdown", "Process interrupted by user")
        print("\n\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        log_system("error", f"Fatal error: {e}", level="CRITICAL", exc_info=True)
        print(f"\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
