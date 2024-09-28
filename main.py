from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get('/hotels')
def get_hotels(
        id_: int | None = Query(None, description="Айди"),
        title: str | None = Query(None, description="Название отеля"),
):
    result = []
    for hotel in hotels:
        if id_ and hotel["id"] != id_:
            continue
        if title and hotel["title"] != title:
            continue
        result.append(hotel)
    return result


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name,
    })
    return {"status": "created"}


@app.put('/hotels/{hotel_id}')
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break

    return {"status": "updated"}


@app.patch("/hotels/{hotel_id}")
def update_hotel_partial(
        hotel_id: int,
        title: str | None = Body(embed=True, default=None),
        name: str | None = Body(embed=True, default=None),
):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            break

    return {"status": "updated"}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    hotels[:] = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
