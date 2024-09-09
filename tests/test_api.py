import os

import pytest

from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_open(monkeypatch):
    original_open = open

    def mock_file_open(path, mode):
        if path == "data.csv":
            path = "tests/data.csv"
        return original_open(path, mode)

    monkeypatch.setattr("builtins.open", mock_file_open)


def test_make_mock():
    with open("tests/data.csv", "w") as fi:
        fi.write("""flight ID,Arrival,Departure,success
A1,08:00,11:00,success
B2,09:00,12:00,fail
C3,10:00,13:00,''
D4,10:00,11:00,''
""")


def test_get_info(client, mock_open):
    result = client.get('/info/A1').json
    assert result["flightID"] == "A1"
    assert result["success"] == "success"
    assert result["status"] == 200

    result = client.get('/info/B2').json
    assert result["flightID"] == "B2"
    assert result["success"] == "fail"
    assert result["status"] == 200

    result = client.get('/info/C3').json
    assert result["flightID"] == "C3"
    assert result["success"] == "success"
    assert result["status"] == 200

    result = client.get('/info/D4').json
    assert result["flightID"] == "D4"
    assert result["success"] == "fail"
    assert result["status"] == 200

    result = client.get('/info/D5').json
    assert result["status"] == 404


def test_update_file(client, mock_open):
    payload = "C1514,11:53,16:00,''".encode("utf-8")
    headers = {
        'Content-Type': 'text/plain'
    }

    response = client.post("/update", headers=headers, data=payload)
    assert response.status_code == 200
    assert response.json == {"status": 200}

    payload = "Bla-lala".encode("utf-8")
    response = client.post("/update", headers=headers, data=payload)
    assert response.status_code == 200
    assert response.json["status"] == 500


def test_clear():
    os.remove("tests/data.csv")
