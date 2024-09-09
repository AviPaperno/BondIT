# BondIT

## Overview

This project is a home assignment for BondIT company. It involves working with flight data, processing it using Python's built-in libraries, and exposing functionality through a Flask API. The project also includes unit tests to ensure code quality, with coverage reporting available.

## Project Features

- **Data Processing**: Utilizes built-in Python libraries like `csv` and `datetime` to handle flight data.
- **API Service**: Implements a REST API using Flask to interact with the flight data.
- **Testing**: Uses `pytest` for testing with optional coverage checking.

## Requirements

- Python 3.8
- Libraries specified in `requirements.txt`
- (Optional) `coverage` for code coverage analysis

## Usage

### Parser

To use the `Parser` class:

```python
from parser import Parser

p = Parser()
```


**Note**: To update data after adding, recreate the Parser object. The data in the .csv file will be cleared and sorted upon object creation.


### API Service

Run the Flask API service by executing:

```shell
python main.py
```

## Testing

To run tests and check coverage:

```shell
coverage run -m pytest
coverage report -m 
```

Current Coverage Report::
```shell
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
main.py                   25      1    96%   34
parser.py                 52      0   100%
tests/__init__.py          0      0   100%
tests/test_api.py         49      0   100%
tests/test_parser.py      37      0   100%
----------------------------------------------------
TOTAL                    163      1    99%

```

## API Endpoints
* **GET** `/flight/{id}`
  * Retrieves information about a specific flight. 
  * Path Parameter: `id` - The ID of the flight.

* **POST** `/flight/update`
  * Updates the CSV file with flight data. 
  * Body: string `format flight ID,Arrival,Departure,success`.


## TODO:

Replace the CSV file with a lightweight database (e.g., SQLite) for better data management, avoiding issues with file locking and concurrency.
