async def test_add_facility(ac):
    title = "Бесплатный Wi-FI"
    response = await ac.post(
        "/facilities/",
        json={"title": title},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["data"]["title"] == title
    assert "data" in response.json()


async def test_get_facilities(ac):
    response = await ac.get("/facilities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
