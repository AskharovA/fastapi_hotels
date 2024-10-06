async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": "2024-10-01",
            "date_to": "2024-10-06"
        }
    )

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "OK"
    assert "data" in result
