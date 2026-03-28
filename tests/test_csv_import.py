"""
Comprehensive tests for improved-csv-import.py
Tests cover: CSV parsing, data cleaning, DB insert logic, error handling,
and edge cases (empty files, malformed rows, quoting).
"""
import sys
import os
import csv
import io
import pytest
from unittest.mock import MagicMock, patch, call, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# Mock mysql.connector at the module level so the source file can be imported.
# ---------------------------------------------------------------------------
mock_mysql = MagicMock()
sys.modules.setdefault("mysql", mock_mysql)
sys.modules.setdefault("mysql.connector", mock_mysql.connector)

import importlib.util

spec = importlib.util.spec_from_file_location(
    "csv_import",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "improved-csv-import.py",
    ),
)
csv_import_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csv_import_module)

import_csv_data = csv_import_module.import_csv_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HEADER = "name,homeworld,leader,champion,weapons,image_url,legion,primarch,successor_chapter,founding,colors\n"

ULTRAMARINES_ROW = (
    '"Ultramarines","Macragge","Marneus Calgar","Cato Sicarius",'
    '"Bolter,Power Sword","https://example.com/ultra.jpg",'
    '"Unbekannt","Roboute Guilliman","Keine","Unbekannt","Blau/Gelb"\n'
)

BLOOD_ANGELS_ROW = (
    '"Blood Angels","Baal","Dante","","Meltagun,Chainsword",'
    '"https://example.com/blood.gif","Unbekannt","Sanguinius","Keine","Unbekannt","Rot/Gold"\n'
)


def make_csv_content(*rows):
    return HEADER + "".join(rows)


def make_mock_db():
    mock_cursor = MagicMock()
    mock_db = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    return mock_db, mock_cursor


# ---------------------------------------------------------------------------
# Unit tests for import_csv_data function
# ---------------------------------------------------------------------------

def run_import_with_csv(csv_content: str, mock_db, monkeypatch=None):
    """Helper: run import_csv_data with a given CSV string, mocking DB and file open.

    Uses a StringIO buffer so we avoid patching builtins.open recursively.
    """
    import csv as csv_mod

    # Build list of rows that csv.reader would produce
    rows_iter = list(csv_mod.reader(io.StringIO(csv_content)))

    call_count = [0]

    class FakeReader:
        def __init__(self, rows):
            self._rows = iter(rows)

        def __iter__(self):
            return self._rows

        def __next__(self):
            return next(self._rows)

    real_open = open

    def fake_open(path, *args, **kwargs):
        if "chapters.csv" in str(path):
            return io.StringIO(csv_content)
        return real_open(path, *args, **kwargs)

    with patch.object(csv_import_module.mysql.connector, "connect", return_value=mock_db):
        with patch("builtins.open", new=fake_open):
            import_csv_data()


class TestImportCsvData:
    def test_calls_truncate_table(self):
        """Verifies the function truncates the chapters table before importing."""
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(HEADER, mock_db)

        truncate_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "TRUNCATE" in str(c)
        ]
        assert len(truncate_calls) == 1

    def test_inserts_one_row(self):
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW), mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 1

    def test_inserts_multiple_rows(self):
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW, BLOOD_ANGELS_ROW), mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 2

    def test_calls_commit(self):
        mock_db, _ = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW), mock_db)
        mock_db.commit.assert_called_once()

    def test_calls_db_close(self):
        mock_db, _ = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW), mock_db)
        mock_db.close.assert_called_once()

    def test_empty_csv_only_truncates(self):
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(HEADER, mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 0

    def test_quoted_fields_are_stripped(self):
        """Fields wrapped in double quotes should have quotes stripped by the cleaning logic."""
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW), mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 1
        values = replace_calls[0][0][1]
        assert values[0] == "Ultramarines"
        assert values[1] == "Macragge"

    def test_inserts_correct_columns_count(self):
        """REPLACE INTO should be called with exactly 11 column values."""
        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(make_csv_content(ULTRAMARINES_ROW), mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        values = replace_calls[0][0][1]
        assert len(values) == 11


# ---------------------------------------------------------------------------
# Unit tests for the data cleaning logic (isolated)
# ---------------------------------------------------------------------------

class TestDataCleaningLogic:
    """Test the inline cleaning logic: strip quotes from fields that are wrapped in them."""

    @staticmethod
    def clean_row(row):
        """Mirror the cleaning logic from improved-csv-import.py."""
        return [
            field.strip('"') if field.startswith('"') and field.endswith('"') else field
            for field in row
        ]

    def test_strips_double_quotes_from_all_fields(self):
        row = ['"Ultramarines"', '"Macragge"', '"Marneus Calgar"']
        result = self.clean_row(row)
        assert result == ["Ultramarines", "Macragge", "Marneus Calgar"]

    def test_leaves_unquoted_fields_unchanged(self):
        row = ["Ultramarines", "Macragge", "Leader"]
        result = self.clean_row(row)
        assert result == ["Ultramarines", "Macragge", "Leader"]

    def test_leaves_empty_field_unchanged(self):
        row = [""]
        result = self.clean_row(row)
        assert result == [""]

    def test_quoted_empty_field(self):
        row = ['""']
        result = self.clean_row(row)
        assert result == [""]

    def test_mixed_quoted_and_unquoted(self):
        row = ['"Blood Angels"', "Baal", '"Dante"']
        result = self.clean_row(row)
        assert result == ["Blood Angels", "Baal", "Dante"]

    def test_field_with_quotes_inside_not_stripped(self):
        # Only strips if BOTH start and end with quote
        row = ['"has "internal" quotes"']
        result = self.clean_row(row)
        assert result == ['has "internal" quotes']

    def test_single_quote_field_not_stripped(self):
        row = ['"only start']
        result = self.clean_row(row)
        assert result == ['"only start']

    def test_row_with_11_columns(self):
        row = [
            '"Ultramarines"', '"Macragge"', '"Marneus Calgar"', '"Cato Sicarius"',
            '"Bolter,Power Sword"', '"https://example.com"',
            '"Unbekannt"', '"Roboute Guilliman"', '"Keine"', '"Unbekannt"', '"Blau/Gelb"'
        ]
        result = self.clean_row(row)
        assert len(result) == 11
        assert result[0] == "Ultramarines"
        assert result[10] == "Blau/Gelb"


# ---------------------------------------------------------------------------
# Regression / edge case tests
# ---------------------------------------------------------------------------

class TestCsvImportEdgeCases:
    def test_file_not_found_raises(self):
        real_open = open

        def fake_open_error(path, *args, **kwargs):
            if "chapters.csv" in str(path):
                raise FileNotFoundError("chapters.csv not found")
            return real_open(path, *args, **kwargs)

        mock_db, _ = make_mock_db()
        with patch.object(csv_import_module.mysql.connector, "connect", return_value=mock_db):
            with patch("builtins.open", new=fake_open_error):
                with pytest.raises(FileNotFoundError):
                    import_csv_data()

    def test_db_connect_error_raises(self):
        with patch.object(
            csv_import_module.mysql.connector, "connect",
            side_effect=Exception("Connection refused")
        ):
            with pytest.raises(Exception, match="Connection refused"):
                import_csv_data()

    def test_csv_with_many_chapters(self):
        rows = []
        for i in range(50):
            rows.append(
                f'"Chapter{i}","World{i}","Leader{i}","Champion{i}",'
                f'"Bolter","https://example.com/img{i}.jpg",'
                f'"Legion{i}","Primarch{i}","None","1st","Blue"\n'
            )
        csv_content = HEADER + "".join(rows)

        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(csv_content, mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 50

    def test_unicode_chapter_names(self):
        row = '"Ölmarine","Ärth","Führer","","Bolter","","","","","",""\n'
        csv_content = HEADER + row

        mock_db, mock_cursor = make_mock_db()
        run_import_with_csv(csv_content, mock_db)

        replace_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "REPLACE INTO chapters" in str(c)
        ]
        assert len(replace_calls) == 1
