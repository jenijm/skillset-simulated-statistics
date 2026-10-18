# Simulated Statistics Assessment: Data Summary Report

## Task brief

Create a command-line program that accepts a small numeric data set and generates a descriptive-statistics report.

### Requirements

- Accept numbers directly in the command, interactively, or from a text/CSV file.
- Support spaces, commas, semicolons, and new lines as separators.
- Calculate count, sum, minimum, maximum, and range.
- Calculate mean, median, and mode.
- Clearly report when a data set has no mode or multiple modes.
- Calculate population variance and standard deviation.
- Calculate sample variance and standard deviation when at least two values exist.
- Validate empty, missing, and non-numeric data.
- Include automated tests and sample data.

## Requirements

- Python 3.8 or newer

No external packages are required.

## Run with command-line numbers

```bash
python3 statistics_report.py 72 85 90 68 85 77 92 85 74 88
```

## Run interactively

```bash
python3 statistics_report.py
```

Enter numbers separated by spaces or commas when prompted.

## Run with the sample CSV file

```bash
python3 statistics_report.py --file data/sample_scores.csv
```

## Run the automated tests

```bash
python3 -m unittest -v
```

The test suite covers calculations, multiple/no modes, single-value data, supported delimiters, CSV input, invalid values, and missing files.
