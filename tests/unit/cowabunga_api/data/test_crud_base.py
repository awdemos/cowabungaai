import pytest
from pydantic import BaseModel, ValidationError
from tests.utils.crud_utils import MockAPIResponse
from tests.mocks.mock_tables import mock_data_model, MockModel

from src.cowabunga_api.data.crud_base import CRUDBase


class MockModelNoID(BaseModel):
    name: str


class MockModelStrID(BaseModel):
    id: str
    name: str


class MockModelFields(BaseModel):
    id: int
    name: str
    created_at: int | str = None
    field_name: str = None


mock_data_dict = dict(id=1, name="mock-data")


def _mock_authed(data):
    return dict(**data, user_id="mock-api-key")


@pytest.fixture
def mock_crud_base(mock_session):
    return CRUDBase(db=mock_session, model=MockModel, table_name="dummy_table")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_data_object, mock_response, expected_result, expected_call",
    [
        (
            mock_data_model,
            mock_data_dict,
            mock_data_model,
            _mock_authed(mock_data_dict),
        ),
        (
            MockModelNoID(name="mock-data"),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(name="mock-data")),
        ),
        (
            MockModelStrID(id="", name="mock-data"),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(name="mock-data")),
        ),
        (
            MockModelFields(id=1, name="mock-data", created_at=0),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(id=1, name="mock-data", field_name=None)),
        ),
        (
            MockModelFields(id=1, name="mock-data", created_at=1),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(id=1, name="mock-data", created_at=1, field_name=None)),
        ),
        (
            MockModelFields(id=1, name="mock-data", created_at="mock-data"),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(id=1, name="mock-data", field_name=None)),
        ),
        (
            MockModelFields(id=1, name="mock-data", field_name="mock-data"),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(id=1, name="mock-data", field_name="mock-data")),
        ),
        (
            MockModelFields(
                id=1, name="mock-data", created_at=0, field_name="mock-data"
            ),
            mock_data_dict,
            mock_data_model,
            _mock_authed(dict(id=1, name="mock-data", field_name="mock-data")),
        ),
    ],
)
async def test_create(
    mock_data_object,
    mock_response,
    expected_result,
    expected_call,
    mock_session,
    mock_crud_base,
):
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.insert.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    result = await mock_crud_base.create(mock_data_object)

    assert result == expected_result
    mock_session.table.assert_called_with(mock_crud_base.table_name)
    if expected_call:
        mock_table.insert.assert_called_with(expected_call)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response",
    [([]), (None)],
)
async def test_create_fail(mock_response, mock_session, mock_crud_base):
    """Empty or None responses return None instead of raising."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.insert.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    result = await mock_crud_base.create(mock_data_model)
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response, expected_result",
    [([dict(id=1, name="mock-data")], MockModel(id=1, name="mock-data")), ([], None)],
)
async def test_get(mock_response, expected_result, mock_session, mock_crud_base):
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    mock_filters = {"id": 1}
    result = await mock_crud_base.get(mock_filters)

    if expected_result:
        assert result == expected_result
    else:
        assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response, expected_error",
    [
        ({"id": 1}, {}, ValidationError),
        (None, {}, ValidationError),
    ],
)
async def test_get_fail(
    filters, mock_response, expected_error, mock_session, mock_crud_base
):
    """Invalid model data still raises ValidationError; None response returns None."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    with pytest.raises(expected_error):
        await mock_crud_base.get(filters)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters",
    [
        ({"id": 1}),
        (None),
    ],
)
async def test_get_none_response(filters, mock_session, mock_crud_base):
    """None response from DB returns None gracefully."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=None
    )

    result = await mock_crud_base.get(filters)
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response, expected_result",
    [
        (
            [dict(id=1, name="mock-data")],
            [MockModel(id=1, name="mock-data")],
        ),
        (
            [dict(id=1, name="mock-data"), dict(id=2, name="mock-data")],
            [MockModel(id=1, name="mock-data"), MockModel(id=2, name="mock-data")],
        ),
        ([], []),
    ],
)
async def test_list(mock_response, expected_result, mock_session, mock_crud_base):
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    result = await mock_crud_base.list({"id": 1})

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, mock_response, expected_error",
    [
        ({"id": 1}, {}, ValidationError),
    ],
)
async def test_list_fail(
    filters, mock_response, expected_error, mock_session, mock_crud_base
):
    """Invalid model data still raises ValidationError; None response returns []."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    with pytest.raises(expected_error):
        await mock_crud_base.list(filters)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters",
    [
        ({"id": 1}),
        ({}),
        (None),
    ],
)
async def test_list_none_response(filters, mock_session, mock_crud_base):
    """None response from DB returns empty list gracefully."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.select.return_value.execute.return_value = MockAPIResponse(
        data=None
    )

    result = await mock_crud_base.list(filters)
    assert result == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response, expected_result", [(mock_data_model, mock_data_model), ([], None)]
)
async def test_update(mock_response, expected_result, mock_session, mock_crud_base):
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.update.return_value.execute.return_value = MockAPIResponse(
        data=mock_response.model_dump() if mock_response else mock_response
    )

    result = await mock_crud_base.update("1", mock_data_model)

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_response", [(None)])
async def test_update_fail(mock_response, mock_session, mock_crud_base):
    """None response from DB returns None gracefully."""
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.update.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    result = await mock_crud_base.update("1", mock_data_model)
    assert result is None


@pytest.mark.asyncio
async def test_delete(mock_crud_base, mock_session):
    mock_table = mock_session.table(mock_crud_base.table_name)

    result = await mock_crud_base.delete({"id": 1})

    assert result is True

    mock_table.delete().eq.assert_any_call("id", 1)


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_response", [([]), (None)])
async def test_delete_fail(mock_response, mock_session, mock_crud_base):
    mock_table = mock_session.table(mock_crud_base.table_name)
    mock_table.delete.return_value.execute.return_value = MockAPIResponse(
        data=mock_response
    )

    result = await mock_crud_base.delete({"id": 1})
    assert result is False
