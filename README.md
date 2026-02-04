# Excel Tag Classifier CLI POC

A Python CLI tool that classifies case summaries from an Excel file into issue tags using Azure OpenAI GPT-5 mini.

## Features

- Read allowed issue tags from the `Tags` sheet
- Classify `Case Summary` values from the `Data` sheet into up to 4 tags
- **Single row mode**: Classify exactly one row by index
- **Batch mode**: Classify multiple rows (by start/limit or explicit indices)
- **Azure Blob Storage Integration**: Process files from Azure Blob Storage automatically
- Robust JSON parsing with retry logic
- CSV and Excel export for results
- Comprehensive logging for debugging and monitoring

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
# Azure OpenAI Configuration
AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_AI_FOUNDRY_KEY=your-api-key
AZURE_AI_FOUNDRY_DEPLOYMENT=gpt-5-mini
AZURE_AI_FOUNDRY_API_VERSION=2025-04-01-preview

# Azure Blob Storage Configuration (for blob processor)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your-account;AccountKey=your-key;EndpointSuffix=core.windows.net
AZURE_BLOB_CONTAINER=your-container-name
```

Or export them directly:

```bash
# Azure OpenAI
export AZURE_AI_FOUNDRY_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_AI_FOUNDRY_KEY="your-api-key"
export AZURE_AI_FOUNDRY_DEPLOYMENT="gpt-5-mini"
export AZURE_AI_FOUNDRY_API_VERSION="2025-04-01-preview"

# Azure Blob Storage
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
export AZURE_BLOB_CONTAINER="your-container-name"
```

### 3. Excel File

Ensure `Example Tags (1).xlsx` is in the project directory with:

- **Tags sheet**: Columns `Issues` (allowed tags) and `Classification` (category mapping)
- **Data sheet**: Column `Case Summary` (text to classify)

## Usage

### Single Row Classification

Classify a single row by its index (0-based):

```bash
python run_poc.py single --row-index 10
```

With custom options:

```bash
python run_poc.py single --row-index 10 --top-k 3 --out result.csv
```

### Batch Classification

Classify multiple rows using start/limit:

```bash
python run_poc.py batch --start 0 --limit 20
```

Classify specific rows by index:

```bash
python run_poc.py batch --row-indices 1,5,9,15
```

Export results to CSV:

```bash
python run_poc.py batch --start 0 --limit 10 --out predictions.csv
```

With throttling between API calls:

```bash
python run_poc.py batch --start 0 --limit 50 --sleep-ms 500
```

With safety guard:

```bash
python run_poc.py batch --start 0 --limit 1000 --max-rows 100
```

## Azure Blob Storage Processing

Process Excel files directly from Azure Blob Storage. Files are automatically:
- Downloaded from the `input` folder
- Processed through the classifier
- Results saved to the `output` folder (both Excel and CSV)
- Original files moved to `archive` folder on success
- Failed files moved to `review` folder for manual inspection

### Folder Structure

The processor uses these folders in your Azure Blob Storage container:
- `input/` - Place Excel files here for processing
- `output/` - Processed results are saved here
- `archive/` - Successfully processed files are moved here
- `review/` - Failed files are moved here for manual review

**Note:** Folders are created automatically on startup. The processor creates `.keep` placeholder files in each folder to ensure they persist even when empty (Azure Blob Storage virtual folders disappear when all blobs are removed).

### Process Mode (One-time)

Process all files in the input folder once:

```bash
python run_blob_processor.py process --container mycontainer
```

With custom folders:

```bash
python run_blob_processor.py process --container mycontainer \
    --input-folder incoming \
    --output-folder results
```

With debug logging:

```bash
python run_blob_processor.py process --container mycontainer --log-level DEBUG
```

### Watch Mode (Continuous)

Continuously poll for new files:

```bash
python run_blob_processor.py watch --container mycontainer --interval 60
```

This will check every 60 seconds for new files in the input folder and process them automatically.

### Blob Processor Options

```
usage: run_blob_processor.py [-h] {process,watch} ...

Process Excel files from Azure Blob Storage through the tag classifier

positional arguments:
  {process,watch}   Available commands
    process         Process all files in input folder once
    watch           Continuously watch for and process new files

Common options (both commands):
  --container       Azure Blob Storage container name (required)
  --input-folder    Input folder name (default: input)
  --output-folder   Output folder name (default: output)
  --archive-folder  Archive folder for processed files (default: archive)
  --review-folder   Review folder for failed files (default: review)
  --data-sheet      Name of data sheet (default: Data)
  --tags-sheet      Name of tags sheet (default: Tags)
  --summary-col     Name of case summary column (default: Case Summary)
  --top-k           Maximum tags per row (default: 4)
  --sleep-ms        Sleep between API calls in ms (default: 0)
  --log-level       Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
  --log-file        Custom log file path (default: logs/processor_YYYYMMDD.log)

Watch command options:
  --interval        Polling interval in seconds (default: 60)
```

### Logging

Logs are stored in the `logs/` directory with daily rotation:
- `logs/processor_20240115.log` (example)

Log format includes timestamps, levels, and context:
```
2024-01-15 10:23:45.123 | INFO     | [file:example.xlsx] [stage:download] Starting download from input/example.xlsx
2024-01-15 10:23:46.456 | INFO     | [file:example.xlsx] [stage:download] Downloaded successfully (245.3 KB)
2024-01-15 10:23:47.890 | INFO     | [file:example.xlsx] [stage:classify] Starting classification (150 rows)
```

Use `--log-level DEBUG` for detailed diagnostics when troubleshooting failures.

---

## Local File Processing

### All Options

```
usage: run_poc.py [-h] {single,batch} ...

Classify Excel case summaries into issue tags using Azure OpenAI

positional arguments:
  {single,batch}  Available commands
    single        Classify a single row
    batch         Classify multiple rows

Common options (both commands):
  --xlsx          Path to Excel file (default: Example Tags (1).xlsx)
  --data-sheet    Name of data sheet (default: Data)
  --tags-sheet    Name of tags sheet (default: Tags)
  --summary-col   Name of case summary column (default: Case Summary)
  --top-k         Maximum number of tags to return (default: 4)
  --out           Output CSV path (optional)

Single command options:
  --row-index     Row index to classify (required, 0-based)

Batch command options:
  --start         Starting row index (default: 0)
  --limit         Number of rows to process (default: 25)
  --row-indices   Comma-separated list of row indices (overrides start/limit)
  --sleep-ms      Sleep between API calls in milliseconds (default: 0)
  --max-rows      Maximum rows to process (guard against large runs)
```

## Output

### Terminal Output

Each classified row displays:
- Row index
- Truncated case summary
- Predicted tags with their classifications
- Needs review flag

### CSV Output

When `--out` is specified, creates a CSV with columns:
- `row_index`
- `pred_tag_1`, `pred_tag_2`, `pred_tag_3`, `pred_tag_4`
- `needs_review`

## Project Structure

```
macu/
├── run_poc.py              # CLI entrypoint for local file processing
├── run_blob_processor.py   # CLI entrypoint for Azure Blob Storage processing
├── blob_storage.py         # Azure Blob Storage operations
├── classifier.py           # Azure OpenAI integration & tag validation
├── data_loader.py          # Load data and row selection logic
├── taxonomy.py             # Load allowed tags from Tags sheet
├── logging_config.py       # Centralized logging configuration
├── terminology_definitions.py  # Tag definitions for prompts
├── requirements.txt        # Dependencies
├── README.md               # This file
├── logs/                   # Log files (auto-created)
└── Example Tags (1).xlsx   # Sample input Excel file
```

## Robustness

- LLM returns JSON: `{ "tags": ["tag1", "tag2", ...] }`
- 0-4 tags, no duplicates, exact matches only
- Invalid tags are dropped
- `needs_review=True` if no valid tags remain
- Up to 3 retries on JSON parse failure before marking needs_review

