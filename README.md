# Excel Tag Classifier CLI POC

A Python CLI tool that classifies case summaries from an Excel file into issue tags using Azure OpenAI GPT-5 mini.

## Features

- Read allowed issue tags from the `Tags` sheet
- Classify `Case Summary` values from the `Data` sheet into up to 4 tags
- **Single row mode**: Classify exactly one row by index
- **Batch mode**: Classify multiple rows (by start/limit or explicit indices)
- Robust JSON parsing with retry logic
- CSV export for results

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_AI_FOUNDRY_KEY=your-api-key
AZURE_AI_FOUNDRY_DEPLOYMENT=gpt-5-mini
AZURE_AI_FOUNDRY_API_VERSION=2025-04-01-preview
```

Or export them directly:

```bash
export AZURE_AI_FOUNDRY_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_AI_FOUNDRY_KEY="your-api-key"
export AZURE_AI_FOUNDRY_DEPLOYMENT="gpt-5-mini"
export AZURE_AI_FOUNDRY_API_VERSION="2025-04-01-preview"
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
├── taxonomy.py         # Load allowed tags from Tags sheet
├── llm_classifier.py   # Azure OpenAI integration & tag validation
├── data_loader.py      # Load data and row selection logic
├── run_poc.py          # CLI entrypoint
├── requirements.txt    # Dependencies
├── README.md           # This file
└── Example Tags (1).xlsx  # Input Excel file
```

## Robustness

- LLM returns JSON: `{ "tags": ["tag1", "tag2", ...] }`
- 0-4 tags, no duplicates, exact matches only
- Invalid tags are dropped
- `needs_review=True` if no valid tags remain
- Up to 3 retries on JSON parse failure before marking needs_review

