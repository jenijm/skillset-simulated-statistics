#!/usr/bin/env python3
"""Generate a descriptive-statistics report for a numeric data set."""

import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Union


Number = Union[int, float]


def calculate_summary(numbers: List[Number]) -> Dict[str, object]:
    """Calculate common descriptive statistics for a non-empty data set."""
    if not numbers:
        raise ValueError("At least one number is required.")

    frequencies = Counter(numbers)
    highest_frequency = max(frequencies.values())
    modes = [] if highest_frequency == 1 else sorted(
        value for value, count in frequencies.items() if count == highest_frequency
    )

    summary = {
        "count": len(numbers),
        "sum": sum(numbers),
        "minimum": min(numbers),
        "maximum": max(numbers),
        "range": max(numbers) - min(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "modes": modes,
        "population_variance": statistics.pvariance(numbers),
        "population_standard_deviation": statistics.pstdev(numbers),
        "sample_variance": None,
        "sample_standard_deviation": None,
    }

    if len(numbers) > 1:
        summary["sample_variance"] = statistics.variance(numbers)
        summary["sample_standard_deviation"] = statistics.stdev(numbers)

    return summary


def parse_number_text(text: str) -> List[float]:
    """Parse numbers separated by commas, spaces, semicolons, or new lines."""
    values = [value for value in re.split(r"[\s,;]+", text.strip()) if value]
    if not values:
        raise ValueError("At least one number is required.")

    try:
        return [float(value) for value in values]
    except ValueError as error:
        raise ValueError("The data contains a value that is not a valid number.") from error


def load_numbers(file_path: Path) -> List[float]:
    """Read and parse numeric data from a text or CSV file."""
    if not file_path.is_file():
        raise ValueError(f"File not found: {file_path}")

    try:
        return parse_number_text(file_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(f"Could not read file: {file_path}") from error


def format_number(value: Optional[Number]) -> str:
    """Format numbers consistently for terminal output."""
    if value is None:
        return "N/A (requires at least 2 values)"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def print_report(numbers: List[Number], summary: Dict[str, object]) -> None:
    """Print a readable statistics report."""
    modes = summary["modes"]
    mode_text = ", ".join(format_number(mode) for mode in modes) if modes else "No mode"

    print("\nDESCRIPTIVE STATISTICS REPORT")
    print("=" * 38)
    print(f"Data: {', '.join(format_number(number) for number in numbers)}")
    print("-" * 38)
    print(f"{'Count:':30} {summary['count']}")
    print(f"{'Sum:':30} {format_number(summary['sum'])}")
    print(f"{'Minimum:':30} {format_number(summary['minimum'])}")
    print(f"{'Maximum:':30} {format_number(summary['maximum'])}")
    print(f"{'Range:':30} {format_number(summary['range'])}")
    print(f"{'Mean:':30} {format_number(summary['mean'])}")
    print(f"{'Median:':30} {format_number(summary['median'])}")
    print(f"{'Mode:':30} {mode_text}")
    print(f"{'Population variance:':30} {format_number(summary['population_variance'])}")
    print(f"{'Population std. deviation:':30} {format_number(summary['population_standard_deviation'])}")
    print(f"{'Sample variance:':30} {format_number(summary['sample_variance'])}")
    print(f"{'Sample std. deviation:':30} {format_number(summary['sample_standard_deviation'])}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Generate a descriptive-statistics report from numeric data."
    )
    parser.add_argument("numbers", nargs="*", help="Numbers separated by spaces.")
    parser.add_argument("--file", type=Path, help="Path to a text or CSV data file.")
    return parser


def main() -> int:
    """Run the report generator."""
    args = build_parser().parse_args()

    try:
        if args.file and args.numbers:
            raise ValueError("Use either command-line numbers or --file, not both.")

        if args.file:
            numbers = load_numbers(args.file)
        elif args.numbers:
            numbers = parse_number_text(" ".join(args.numbers))
        else:
            entered = input("Enter numbers separated by spaces or commas: ")
            numbers = parse_number_text(entered)

        summary = calculate_summary(numbers)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_report(numbers, summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
