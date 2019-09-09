import pytest

QUERY = "SELECT * FROM players;"


@pytest.fixture
def db_connection():
    from crael.connection import SQLDataBase
    return SQLDataBase()


def test_execute_query(db_connection, query=QUERY):
    """
    Test if the query returns aa valid list
    placeholder.
    """
    pass
