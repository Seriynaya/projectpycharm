from unittest.mock import Mock, mock_open, patch

import pandas as pd

from src.open_file import read_csv_file, read_excel_file


@patch('csv.reader')
def test_read_csv_file(mock_read):
    m = mock_open()
    mock_read.return_value = [{
        'id': '650703',
        'state': 'EXECUTED',
        'date': '2023-09-05T11:30:32Z',
        'amount': '16210'
    }]

    with patch('builtins.open', m) as mocked_open:
        assert read_csv_file('transaction.csv') == [{
            'id': '650703',
            'state': 'EXECUTED',
            'date': '2023-09-05T11:30:32Z',
            'amount': '16210'
        }]

        mocked_open.assert_called_with('transaction.csv', 'r', encoding='utf-8')
