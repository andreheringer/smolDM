import pytest

QUERY = "SELECT * FROM players;"


@pytest.fixture
def db_connection():
    from src.connection import SQLDataBase
    return SQLDataBase()


def test_execute_query(db_connection, query=QUERY):
    """
    Test if the query returns aa valid list
    """
    with db_connection as db:
        cur = db.get_cursor()
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
        assert rows != []
