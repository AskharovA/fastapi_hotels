async def test_add_facility(ac):
    response = await ac.post(
        "/facilities/",
        json={"title": "Бесплатный Wi-FI"},
    )
    assert response.status_code == 200


async def test_get_facility(ac):
    response = await ac.get("/facilities/")
    assert response.status_code == 200
