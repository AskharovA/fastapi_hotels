async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels", params={"date_from": "2024-10-01", "date_to": "2024-10-06"}
    )

    assert response.status_code == 200
