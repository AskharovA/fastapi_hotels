import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@gmail.com", "12345678", 200),
        ("user2@gmail.com", "65756755", 200),
        ("user1@gmail.com", "53453465", 409),
        ("user3#gmail.com", "88768767", 422),
        ("user4@gmail.com", "88768767", 200),
    ],
)
async def test_auth(email, password, status_code, ac):
    user_data = {"email": email, "password": password}

    response = await ac.post("/auth/register", json=user_data)
    assert response.status_code == status_code

    if response.status_code != 200:
        return

    await ac.post("/auth/login", json=user_data)
    assert ac.cookies["access_token"]

    response = await ac.get("/auth/me")
    user_data = response.json()
    assert user_data["email"] == email
    assert "id" in user_data
    assert "password" not in user_data
    assert "hashed_password" not in user_data

    response = await ac.delete("/auth/logout")
    assert response.json()["status"] == "OK"
    assert ac.cookies.get("access_token", None) is None

    response = await ac.get("/auth/me")
    assert response.status_code == 401
