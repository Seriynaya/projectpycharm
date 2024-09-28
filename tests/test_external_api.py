from unittest.mock import patch

from src.external_api import convert_from_i_to_rub

transaction = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
        "amount": "8000",
        "currency": {
            "name": "USD",
            "code": "USD"
        }}}


@patch("requests.get")
def test_convert_from_i_to_rub(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'success': True, 'timestamp': 1720199764, 'base': 'USD',
                                               'date': '2024-07-05',
                                               'rates': {'RUB': 100}}
    mock_get.get.return_value = mock_get
    print(mock_get.get.return_value)
    assert convert_from_i_to_rub(transaction) == 800000.0
