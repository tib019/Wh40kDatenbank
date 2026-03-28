"""
Comprehensive tests for improved-flask-api.py
Tests cover: all routes, status codes, response shapes, error handling,
DB mock interactions, CORS headers, and regression/edge cases.
"""
import sys
import os
import json
import pytest
from unittest.mock import MagicMock, patch, call

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# We need to mock mysql.connector at the module level BEFORE importing the app
# so the import of 'improved-flask-api' doesn't attempt a real DB connection.
# ---------------------------------------------------------------------------

mock_mysql = MagicMock()
sys.modules["mysql"] = mock_mysql
sys.modules["mysql.connector"] = mock_mysql.connector

import importlib.util
spec = importlib.util.spec_from_file_location(
    "flask_api",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "improved-flask-api.py"),
)
flask_api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flask_api_module)
app = flask_api_module.app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_CHAPTERS = [
    {
        "id": 1,
        "name": "Ultramarines",
        "homeworld": "Macragge",
        "leader": "Marneus Calgar",
        "champion": "Cato Sicarius",
        "weapons": "Bolter,Power Sword",
        "image_url": "https://example.com/ultra.jpg",
        "legion": "Unbekannt",
        "primarch": "Roboute Guilliman",
        "successor_chapter": "Keine",
        "founding": "Unbekannt",
        "colors": "Blau/Gelb",
    },
    {
        "id": 2,
        "name": "Blood Angels",
        "homeworld": "Baal",
        "leader": "Dante",
        "champion": "",
        "weapons": "Meltagun,Chainsword",
        "image_url": "https://example.com/blood.jpg",
        "legion": "Unbekannt",
        "primarch": "Sanguinius",
        "successor_chapter": "Keine",
        "founding": "Unbekannt",
        "colors": "Rot/Gold",
    },
]


def make_mock_db(fetchall_result=None, fetchone_result=None):
    """Create a mock db connection with a configured cursor."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fetchall_result or []
    mock_cursor.fetchone.return_value = fetchone_result

    mock_db = MagicMock()
    mock_db.cursor.return_value = mock_cursor

    return mock_db, mock_cursor


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# GET /chapters
# ---------------------------------------------------------------------------

class TestGetAllChapters:
    def test_returns_200(self, client):
        mock_db, _ = make_mock_db(fetchall_result=SAMPLE_CHAPTERS)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        assert response.status_code == 200

    def test_returns_json_list(self, client):
        mock_db, _ = make_mock_db(fetchall_result=SAMPLE_CHAPTERS)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_chapter_fields_present(self, client):
        mock_db, _ = make_mock_db(fetchall_result=SAMPLE_CHAPTERS)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        data = json.loads(response.data)
        chapter = data[0]
        assert chapter["name"] == "Ultramarines"
        assert chapter["homeworld"] == "Macragge"
        assert "id" in chapter

    def test_empty_db_returns_empty_list(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_db_close_is_called(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters")
        mock_db.close.assert_called_once()

    def test_cursor_uses_dictionary_mode(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters")
        mock_db.cursor.assert_called_once_with(dictionary=True)

    def test_content_type_is_json(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        assert "application/json" in response.content_type

    def test_single_chapter_returned(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        data = json.loads(response.data)
        assert len(data) == 1


# ---------------------------------------------------------------------------
# GET /chapters/<int:id>
# ---------------------------------------------------------------------------

class TestGetChapterById:
    def test_returns_200_for_existing_id(self, client):
        mock_db, _ = make_mock_db(fetchone_result=SAMPLE_CHAPTERS[0])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/1")
        assert response.status_code == 200

    def test_returns_correct_chapter_data(self, client):
        mock_db, _ = make_mock_db(fetchone_result=SAMPLE_CHAPTERS[0])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/1")
        data = json.loads(response.data)
        assert data["name"] == "Ultramarines"
        assert data["id"] == 1

    def test_returns_404_for_missing_id(self, client):
        mock_db, _ = make_mock_db(fetchone_result=None)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/999")
        assert response.status_code == 404

    def test_404_response_body(self, client):
        mock_db, _ = make_mock_db(fetchone_result=None)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/999")
        assert b"Not found" in response.data

    def test_id_zero_returns_404_when_not_found(self, client):
        mock_db, _ = make_mock_db(fetchone_result=None)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/0")
        assert response.status_code == 404

    def test_db_close_is_called(self, client):
        mock_db, _ = make_mock_db(fetchone_result=SAMPLE_CHAPTERS[0])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters/1")
        mock_db.close.assert_called_once()

    def test_query_uses_correct_id(self, client):
        mock_db, mock_cursor = make_mock_db(fetchone_result=SAMPLE_CHAPTERS[1])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters/2")
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert 2 in call_args or (2,) in call_args

    def test_invalid_id_type_returns_404(self, client):
        response = client.get("/chapters/abc")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /chapters/name/<string:chapter_name>
# ---------------------------------------------------------------------------

class TestGetChapterByName:
    def test_returns_200_for_existing_name(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/ultramarines")
        assert response.status_code == 200

    def test_returns_json_list(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/Ultramarines")
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert data[0]["name"] == "Ultramarines"

    def test_case_insensitive_search_via_like(self, client):
        """The query uses LIKE %name%, so any casing in the path param is passed through."""
        mock_db, mock_cursor = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters/name/ultramarines")
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        # The param passed to LIKE should contain the search term
        assert any("ultramarines" in str(arg).lower() for arg in call_args)

    def test_returns_404_when_not_found(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/nonexistent")
        assert response.status_code == 404

    def test_returns_404_body(self, client):
        mock_db, _ = make_mock_db(fetchall_result=None)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/doesnotexist")
        assert response.status_code == 404
        assert b"Not found" in response.data

    def test_partial_name_match(self, client):
        mock_db, mock_cursor = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/ultra")
        assert response.status_code == 200
        # Verify LIKE query was used with wildcards
        call_args = mock_cursor.execute.call_args[0]
        assert any("%ultra%" in str(arg) for arg in call_args)

    def test_db_close_is_called(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            client.get("/chapters/name/test")
        mock_db.close.assert_called_once()

    def test_returns_multiple_matching_chapters(self, client):
        mock_db, _ = make_mock_db(fetchall_result=SAMPLE_CHAPTERS)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/angels")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2


# ---------------------------------------------------------------------------
# CORS headers
# ---------------------------------------------------------------------------

class TestCorsHeaders:
    def test_cors_header_on_chapters_endpoint(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        assert response.headers.get("Access-Control-Allow-Origin") == "*"

    def test_cors_methods_header(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")
        methods = response.headers.get("Access-Control-Allow-Methods", "")
        assert "GET" in methods


# ---------------------------------------------------------------------------
# Image proxy
# ---------------------------------------------------------------------------

class TestImageProxy:
    def test_missing_url_param_returns_400(self, client):
        response = client.get("/api/image-proxy")
        assert response.status_code == 400

    def test_external_request_error_returns_500(self, client):
        with patch("requests.get", side_effect=Exception("network error")):
            response = client.get("/api/image-proxy?url=https://example.com/img.jpg")
        assert response.status_code == 500


# ---------------------------------------------------------------------------
# Functional tests: full request/response cycle with mocked MySQL
# ---------------------------------------------------------------------------

class TestFunctionalCycle:
    def test_full_get_chapters_cycle(self, client):
        """Simulate a real app request: verify DB is queried and JSON returned."""
        mock_db, mock_cursor = make_mock_db(fetchall_result=SAMPLE_CHAPTERS)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters")

        assert response.status_code == 200
        mock_cursor.execute.assert_called_once_with("SELECT * FROM chapters")
        mock_cursor.fetchall.assert_called_once()
        mock_db.close.assert_called_once()
        data = json.loads(response.data)
        assert len(data) == 2

    def test_full_get_chapter_by_id_cycle(self, client):
        mock_db, mock_cursor = make_mock_db(fetchone_result=SAMPLE_CHAPTERS[0])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/1")

        assert response.status_code == 200
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_db.close.assert_called_once()

    def test_full_get_chapter_by_name_cycle(self, client):
        mock_db, mock_cursor = make_mock_db(fetchall_result=[SAMPLE_CHAPTERS[0]])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/Ultramarines")

        assert response.status_code == 200
        mock_cursor.execute.assert_called_once()
        mock_db.close.assert_called_once()


# ---------------------------------------------------------------------------
# Regression tests: invalid IDs, missing params, DB errors
# ---------------------------------------------------------------------------

class TestRegression:
    def test_very_large_id_returns_404(self, client):
        mock_db, _ = make_mock_db(fetchone_result=None)
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/9999999999")
        assert response.status_code == 404

    def test_negative_id_not_found(self, client):
        # Flask int converter doesn't accept negative integers; expect 404 from routing
        response = client.get("/chapters/-1")
        assert response.status_code == 404

    def test_empty_name_search_returns_result_or_404(self, client):
        # Empty string after /name/ is a valid route that matches everything or nothing
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/ ")
        # Either 200 (empty list edge case handled) or 404 — not a 500
        assert response.status_code in (200, 404)

    def test_special_chars_in_name_dont_cause_500(self, client):
        mock_db, _ = make_mock_db(fetchall_result=[])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/blood%20angels")
        assert response.status_code in (200, 404)

    def test_db_connection_error_raises_exception(self):
        """When db_connection raises, Flask (in TESTING mode) re-raises the exception.
        In production it would return a 500. We verify the exception propagates."""
        app.config["TESTING"] = True
        with app.test_client() as c:
            with patch.object(
                flask_api_module, "db_connection", side_effect=Exception("DB unavailable")
            ):
                with pytest.raises(Exception, match="DB unavailable"):
                    c.get("/chapters")

    def test_method_not_allowed_on_chapters(self, client):
        response = client.post("/chapters")
        assert response.status_code == 405

    def test_chapters_name_returns_json_with_all_fields(self, client):
        chapter = SAMPLE_CHAPTERS[0].copy()
        mock_db, _ = make_mock_db(fetchall_result=[chapter])
        with patch.object(flask_api_module, "db_connection", return_value=mock_db):
            response = client.get("/chapters/name/Ultramarines")
        data = json.loads(response.data)
        assert len(data) == 1
        for field in ("id", "name", "homeworld", "leader", "primarch"):
            assert field in data[0]
