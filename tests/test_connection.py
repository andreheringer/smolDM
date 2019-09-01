import asyncio
import pytest
import pytest_asyncio


QUERY = "SELECT COUNT(DISTINCT `table_name`) FROM `information_schema`.`columns` WHERE `table_schema` = 'crael';"


@pytest.mark.asyncio
async def test_execute_query(query=QUERY):
    """
        Placeholder
    """
    assert True

@pytest.mark.asyncio
async def test_get_schema():
    """
        Placeholder
    """
    assert True

@pytest.mark.asyncio
async def test_execute_script():
    """
        Placeholder
    """
    assert True