import os

import pytest

from parser import Parser

FILEPATH = "tests/data.csv"


@pytest.fixture
def mock_open(monkeypatch):
    original_open = open

    def mock_file_open(path, mode):
        if path == "data.csv":
            path = "tests/data.csv"
        return original_open(path, mode)

    monkeypatch.setattr("builtins.open", mock_file_open)


def test_make_mock():
    with open(FILEPATH, "w") as fi:
        fi.write("""flight ID,Arrival,Departure,success
A1,08:00,11:00,success
B2,09:00,12:00,fail
C3,10:00,13:00,''
D4,10:00,11:00,''
""")


def test_init_parser(mock_open):
    parser_instance = Parser()
    assert parser_instance.data["A1"]["success"] is True
    assert parser_instance.data["B2"]["success"] is False
    assert parser_instance.data["C3"]["success"] is True
    assert parser_instance.data["D4"]["success"] is False


def test_update_parser(mock_open):
    parser_instance = Parser()
    parser_instance.add_field("E5,7:00,11:00,''")
    parser_instance.add_field("F6,10:02,11:00,''")
    parser_instance = Parser()
    assert parser_instance.data["E5"]["success"] is True
    assert parser_instance.data["F6"]["success"] is False


def test_update_many(mock_open):
    parser_instance = Parser()
    for i in range(10):
        parser_instance.add_field(f"TMP_0{i},9:0{i},15:00,''")
        parser_instance.add_field(f"TMP_1{i},9:1{i},15:30,''")
    parser_instance = Parser()
    assert parser_instance.data["C3"]["success"] is False


def test_clear(mock_open):
    os.remove("tests/data.csv")
