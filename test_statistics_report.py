"""Tests for the descriptive-statistics report generator."""

import tempfile
import unittest
from pathlib import Path

from statistics_report import build_parser, calculate_summary, load_numbers, parse_number_text


class StatisticsReportTests(unittest.TestCase):
    def test_calculates_complete_summary(self):
        result = calculate_summary([2, 4, 4, 6, 8])

        self.assertEqual(result["count"], 5)
        self.assertEqual(result["sum"], 24)
        self.assertEqual(result["minimum"], 2)
        self.assertEqual(result["maximum"], 8)
        self.assertEqual(result["range"], 6)
        self.assertEqual(result["mean"], 4.8)
        self.assertEqual(result["median"], 4)
        self.assertEqual(result["modes"], [4])
        self.assertAlmostEqual(result["population_variance"], 4.16)

    def test_reports_multiple_modes(self):
        result = calculate_summary([1, 1, 2, 2, 3])
        self.assertEqual(result["modes"], [1, 2])

    def test_reports_no_mode_when_every_value_is_unique(self):
        result = calculate_summary([1, 2, 3, 4])
        self.assertEqual(result["modes"], [])

    def test_single_value_has_no_sample_statistics(self):
        result = calculate_summary([7])
        self.assertIsNone(result["sample_variance"])
        self.assertIsNone(result["sample_standard_deviation"])

    def test_parses_multiple_delimiters(self):
        self.assertEqual(
            parse_number_text("1, 2.5; -3\n4"),
            [1.0, 2.5, -3.0, 4.0],
        )

    def test_loads_csv_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "values.csv"
            file_path.write_text("10,20,20,30", encoding="utf-8")
            self.assertEqual(load_numbers(file_path), [10.0, 20.0, 20.0, 30.0])

    def test_rejects_empty_data(self):
        with self.assertRaises(ValueError):
            calculate_summary([])
        with self.assertRaises(ValueError):
            parse_number_text("  ")

    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            parse_number_text("1, two, 3")

    def test_rejects_missing_file(self):
        with self.assertRaises(ValueError):
            load_numbers(Path("missing-data.csv"))

    def test_command_line_parser_supports_numbers_and_files(self):
        number_args = build_parser().parse_args(["1", "2", "3"])
        file_args = build_parser().parse_args(["--file", "scores.csv"])

        self.assertEqual(number_args.numbers, ["1", "2", "3"])
        self.assertIsNone(number_args.file)
        self.assertEqual(file_args.file, Path("scores.csv"))
        self.assertEqual(file_args.numbers, [])


if __name__ == "__main__":
    unittest.main()
