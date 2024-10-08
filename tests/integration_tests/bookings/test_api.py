import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        (1, "2024-08-06", "2024-08-15", 409),
        (1, "2024-08-17", "2024-08-25", 200),
        (1, "2024-08-17", "2024-08-16", 422),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        assert isinstance(result, dict)
        assert result["status"] == "OK"
        assert "data" in result


@pytest.fixture(scope="module")
async def delete_all_bookings():
    from tests.conftest import get_db_null_pool

    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-11", "2024-08-16", 2),
        (1, "2024-08-17", "2024-08-21", 3),
        (1, "2024-08-22", "2024-08-28", 4),
    ],
)
async def test_add_and_get_my_booking(
    room_id, date_from, date_to, count, delete_all_bookings, db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    my_bookings = await authenticated_ac.get("/bookings/me")
    assert my_bookings.status_code == 200
    assert len(my_bookings.json()) == count
