# Multi-File Transaction Processing Pipeline

A small Python data-processing pipeline that discovers transaction CSV files,
validates their contents, cleans valid records, and writes consolidated output
files.

The complete pipeline is implemented in [`step.py`](./step.py). It is designed
to process multiple daily transaction files from one input directory.

## What the pipeline does

For each file matching `transactions_*.csv`, the pipeline:

1. Discovers files in stable filename order.
2. Reads the CSV and records the source filename for every row.
3. Checks that all required columns are present.
4. Validates required values, quantities, prices, and transaction ID
   uniqueness.
5. Strips surrounding whitespace and converts `quantity` and `unit_price` to
   numbers for valid rows.
6. Writes valid transactions, rejected transactions, and a processing summary.

Files with missing required columns are skipped as input files, and every row
from those files is written to the rejected output with the missing-column
reason.

## Requirements

- Python 3.9 or newer
- The packages listed in [`requirements.txt`](./requirements.txt)

The current implementation uses the Python standard library and imports
`pandas`; installing the requirements file ensures the project environment is
available for future pipeline extensions as well.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the pipeline with the default directories:

```bash
python step.py
```

By default:

- Input files are read from `data/`
- Output files are written to `output/`

Custom input and output directories can be supplied:

```bash
python step.py --input path/to/input --output path/to/output
```

For example, on Windows:

```powershell
python .\step.py --input .\data --output .\output
```

The command logs file-level errors and exits with status `1` when the pipeline
cannot start because of an input-directory or other top-level file error.
Validation failures for individual rows are captured in the rejected CSV
instead of stopping the complete run.

## Input files

Input filenames must match:

```text
transactions_*.csv
```

Each file must contain these required columns:

| Column | Description |
| --- | --- |
| `transaction_id` | Unique transaction identifier across all input files |
| `date` | Transaction date |
| `branch` | Branch where the transaction occurred |
| `customer_id` | Customer identifier |
| `product` | Product description |
| `quantity` | Positive numeric quantity |
| `unit_price` | Positive numeric unit price |
| `payment_method` | Payment method used |

Additional columns are allowed. They are read but are not included in the
consolidated output. For example, `payment_ref` and `cashier` may be present in
source files without changing the output schema.

## Validation rules

A row is rejected when:

- A required value is missing or blank.
- `quantity` is non-numeric or less than or equal to zero.
- `unit_price` is non-numeric or less than or equal to zero.
- `transaction_id` has already appeared in a previously accepted row.

Transaction IDs are added to the duplicate-check set only after a row passes
all other validation checks. Rejected rows therefore do not reserve an ID.

## Output files

The output directory contains:

### `consolidated_transactions.csv`

Contains accepted transactions with:

- The eight required transaction columns
- `_source_file`, identifying the input file for each row

### `rejected_transactions.csv`

Contains rejected rows and:

- `_source_file`, identifying the input file
- `_rejection_reason`, describing one or more validation failures

### `summary.txt`

Contains counts for:

- Files discovered
- Files processed
- Files rejected
- Rows read
- Valid transactions
- Rejected transactions

Existing output files are overwritten on each run. Output directories are
created automatically when they do not exist.

## Sample data and result

The repository includes three sample files in [`data/`](./data/). Running:

```bash
python step.py
```

produces the sample output currently summarized as:

```text
Files discovered: 3
Files processed: 2
Files rejected: 1
Rows read: 43
Valid transactions: 24
Rejected transactions: 19
```

The third sample file is rejected because it uses `qty` instead of the
required `quantity` column.

## Project structure

```text
.
├── data/
│   ├── transactions_2026-10-01.csv
│   ├── transactions_2026-10-02.csv
│   └── transactions_2026-10-03.csv
├── output/
│   ├── consolidated_transactions.csv
│   ├── rejected_transactions.csv
│   └── summary.txt
├── pipeline.py
├── requirements.txt
├── step.py
└── README.md
```

`pipeline.py` contains a small file-discovery example. Use `step.py` as the
executable end-to-end pipeline.
