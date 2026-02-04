"""
blob_storage.py - Azure Blob Storage operations for the Excel tag classifier.

Provides functions to list, download, upload, move, and delete blobs
from Azure Blob Storage containers.
"""

import os
from io import BytesIO
from typing import List, Optional, Tuple

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError, AzureError

from logging_config import log_system, get_file_logger


def get_blob_service_client() -> BlobServiceClient:
    """
    Create an Azure Blob Service client using connection string from environment.
    
    Required env var:
        - AZURE_STORAGE_CONNECTION_STRING
    
    Returns:
        BlobServiceClient instance
    
    Raises:
        ValueError: If connection string is not set
        AzureError: If connection fails
    """
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    
    if not connection_string:
        log_system("connection", "AZURE_STORAGE_CONNECTION_STRING not set", level="CRITICAL")
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")
    
    try:
        client = BlobServiceClient.from_connection_string(connection_string)
        log_system("connection", "Azure Blob Service client created successfully")
        return client
    except AzureError as e:
        log_system("connection", f"Failed to create Azure Blob Service client: {e}", level="CRITICAL", exc_info=True)
        raise


def get_container_client(container_name: str) -> ContainerClient:
    """
    Get a container client for the specified container.
    
    Args:
        container_name: Name of the Azure Blob Storage container
    
    Returns:
        ContainerClient instance
    """
    service_client = get_blob_service_client()
    container_client = service_client.get_container_client(container_name)
    log_system("connection", f"Container client created", container=container_name)
    return container_client


def list_input_blobs(
    container_name: str,
    input_folder: str = "input",
    file_extension: str = ".xlsx"
) -> List[str]:
    """
    List all Excel files in the input folder.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        input_folder: Name of the input folder (default: "input")
        file_extension: File extension to filter by (default: ".xlsx")
    
    Returns:
        List of blob names (full paths including folder prefix)
    """
    log_system("list", f"Listing blobs in {input_folder}/", container=container_name)
    
    try:
        container_client = get_container_client(container_name)
        prefix = f"{input_folder}/" if not input_folder.endswith("/") else input_folder
        
        blobs = []
        for blob in container_client.list_blobs(name_starts_with=prefix):
            blob_name = blob.name
            # Skip folder markers, placeholder files, and non-matching extensions
            if blob_name.endswith("/"):
                continue
            if blob_name.endswith(".keep"):
                continue
            if file_extension and not blob_name.lower().endswith(file_extension.lower()):
                continue
            blobs.append(blob_name)
        
        log_system("list", f"Found {len(blobs)} {file_extension} files in {input_folder}/", container=container_name)
        return blobs
    
    except AzureError as e:
        log_system("list", f"Failed to list blobs: {e}", level="ERROR", exc_info=True)
        raise


def download_blob_to_bytes(container_name: str, blob_name: str) -> Tuple[bytes, int]:
    """
    Download a blob and return its contents as bytes.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        blob_name: Full path to the blob (e.g., "input/example.xlsx")
    
    Returns:
        Tuple of (blob_bytes, size_in_bytes)
    
    Raises:
        ResourceNotFoundError: If blob doesn't exist
        AzureError: If download fails
    """
    filename = os.path.basename(blob_name)
    file_logger = get_file_logger(filename)
    
    file_logger.info("download", f"Starting download from {blob_name}")
    
    try:
        container_client = get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        # Download blob data
        download_stream = blob_client.download_blob()
        blob_bytes = download_stream.readall()
        size_bytes = len(blob_bytes)
        size_kb = size_bytes / 1024
        
        file_logger.info("download", f"Downloaded successfully ({size_kb:.1f} KB)")
        
        return blob_bytes, size_bytes
    
    except ResourceNotFoundError:
        file_logger.error("download", f"Blob not found: {blob_name}", exc_info=False)
        raise
    except AzureError as e:
        file_logger.error("download", f"Failed to download blob: {e}")
        raise


def upload_blob(
    container_name: str,
    blob_name: str,
    data: bytes,
    overwrite: bool = True
) -> int:
    """
    Upload data to a blob.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        blob_name: Full path for the blob (e.g., "output/example_predictions.xlsx")
        data: Bytes to upload
        overwrite: Whether to overwrite existing blob (default: True)
    
    Returns:
        Size of uploaded data in bytes
    
    Raises:
        AzureError: If upload fails
    """
    filename = os.path.basename(blob_name)
    file_logger = get_file_logger(filename)
    
    size_bytes = len(data)
    size_kb = size_bytes / 1024
    
    file_logger.info("upload", f"Uploading to {blob_name} ({size_kb:.1f} KB)")
    
    try:
        container_client = get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.upload_blob(data, overwrite=overwrite)
        
        file_logger.info("upload", f"Uploaded successfully to {blob_name}")
        return size_bytes
    
    except AzureError as e:
        file_logger.error("upload", f"Failed to upload blob: {e}")
        raise


def move_blob(
    container_name: str,
    source_blob_name: str,
    destination_blob_name: str
) -> None:
    """
    Move a blob from source to destination (download + upload + delete).
    
    Uses download/upload pattern instead of copy URL to ensure authentication
    works correctly regardless of container access settings.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        source_blob_name: Full path of source blob
        destination_blob_name: Full path of destination blob
    
    Raises:
        ResourceNotFoundError: If source blob doesn't exist
        AzureError: If move operation fails
    """
    filename = os.path.basename(source_blob_name)
    file_logger = get_file_logger(filename)
    
    file_logger.info("move", f"Moving from {source_blob_name} to {destination_blob_name}")
    
    try:
        container_client = get_container_client(container_name)
        
        # Get source and destination blob clients
        source_blob = container_client.get_blob_client(source_blob_name)
        dest_blob = container_client.get_blob_client(destination_blob_name)
        
        # Download the source blob content
        download_stream = source_blob.download_blob()
        blob_data = download_stream.readall()
        
        # Upload to destination
        dest_blob.upload_blob(blob_data, overwrite=True)
        
        # Delete the source blob
        source_blob.delete_blob()
        
        file_logger.info("move", f"Moved successfully to {destination_blob_name}")
    
    except ResourceNotFoundError:
        file_logger.error("move", f"Source blob not found: {source_blob_name}", exc_info=False)
        raise
    except AzureError as e:
        file_logger.error("move", f"Failed to move blob: {e}")
        raise


def delete_blob(container_name: str, blob_name: str) -> None:
    """
    Delete a blob.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        blob_name: Full path to the blob
    
    Raises:
        ResourceNotFoundError: If blob doesn't exist
        AzureError: If delete fails
    """
    filename = os.path.basename(blob_name)
    file_logger = get_file_logger(filename)
    
    file_logger.info("delete", f"Deleting blob: {blob_name}")
    
    try:
        container_client = get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.delete_blob()
        
        file_logger.info("delete", f"Deleted successfully: {blob_name}")
    
    except ResourceNotFoundError:
        file_logger.warning("delete", f"Blob not found (may already be deleted): {blob_name}", exc_info=False)
    except AzureError as e:
        file_logger.error("delete", f"Failed to delete blob: {e}")
        raise


def move_to_review(container_name: str, source_blob_name: str, review_folder: str = "review") -> str:
    """
    Move a blob to the review folder.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        source_blob_name: Full path of source blob (e.g., "input/example.xlsx")
        review_folder: Name of the review folder (default: "review")
    
    Returns:
        Path to the blob in the review folder
    """
    filename = os.path.basename(source_blob_name)
    file_logger = get_file_logger(filename)
    
    destination = f"{review_folder}/{filename}"
    
    file_logger.warning("review", f"Moving file to review folder due to processing failure")
    
    try:
        move_blob(container_name, source_blob_name, destination)
        file_logger.info("review", f"File moved to {destination}")
        return destination
    except Exception as e:
        file_logger.error("review", f"Failed to move to review folder: {e}")
        raise


def move_to_archive(container_name: str, source_blob_name: str, archive_folder: str = "archive") -> str:
    """
    Move a blob to the archive folder after successful processing.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        source_blob_name: Full path of source blob (e.g., "input/example.xlsx")
        archive_folder: Name of the archive folder (default: "archive")
    
    Returns:
        Path to the blob in the archive folder
    """
    filename = os.path.basename(source_blob_name)
    file_logger = get_file_logger(filename)
    
    destination = f"{archive_folder}/{filename}"
    
    file_logger.info("archive", f"Moving file to archive folder")
    
    try:
        move_blob(container_name, source_blob_name, destination)
        file_logger.info("archive", f"File archived to {destination}")
        return destination
    except Exception as e:
        file_logger.error("archive", f"Failed to move to archive folder: {e}")
        raise


def ensure_folders_exist(
    container_name: str,
    folders: List[str] = None
) -> List[str]:
    """
    Ensure required folders exist by creating .keep placeholder files.
    
    Azure Blob Storage uses virtual folders that disappear when empty.
    This function creates a .keep file in each folder to persist them.
    
    Args:
        container_name: Name of the Azure Blob Storage container
        folders: List of folder names to ensure exist.
                 Defaults to ["input", "output", "archive", "review"]
    
    Returns:
        List of folders that were created or already existed
    """
    if folders is None:
        folders = ["input", "output", "archive", "review"]
    
    log_system("folders", f"Ensuring folders exist: {folders}", container=container_name)
    
    try:
        container_client = get_container_client(container_name)
        created_folders = []
        
        for folder in folders:
            folder_name = folder.rstrip("/")
            keep_file_path = f"{folder_name}/.keep"
            
            blob_client = container_client.get_blob_client(keep_file_path)
            
            # Check if .keep file already exists
            try:
                blob_client.get_blob_properties()
                log_system("folders", f"Folder '{folder_name}/' already exists", level="DEBUG")
            except ResourceNotFoundError:
                # Create the .keep file
                keep_content = f"# Placeholder file to persist the {folder_name} folder\n"
                blob_client.upload_blob(keep_content.encode('utf-8'), overwrite=True)
                log_system("folders", f"Created folder '{folder_name}/' with .keep placeholder")
            
            created_folders.append(folder_name)
        
        log_system("folders", f"All {len(created_folders)} folders verified/created")
        return created_folders
    
    except AzureError as e:
        log_system("folders", f"Failed to ensure folders exist: {e}", level="ERROR", exc_info=True)
        raise


if __name__ == "__main__":
    # Quick test (requires AZURE_STORAGE_CONNECTION_STRING to be set)
    from dotenv import load_dotenv
    from logging_config import setup_logging
    
    load_dotenv()
    setup_logging(level="DEBUG")
    
    container = os.environ.get("AZURE_BLOB_CONTAINER", "test-container")
    
    print(f"\nTesting blob storage operations with container: {container}")
    print("-" * 60)
    
    try:
        # List blobs
        blobs = list_input_blobs(container)
        print(f"Found {len(blobs)} Excel files in input/")
        for blob in blobs:
            print(f"  - {blob}")
    except Exception as e:
        print(f"Error: {e}")
