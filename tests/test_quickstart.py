from unittest.mock import patch

from  quickstart import main


def test_files():
    with patch('quickstart.build') as qb:
        qb().files().list().execute.return_value = {
            'files': [{'name': 'foo'}, {'name': 'bar'}]
        }
        items = main()
    assert items
