# Hotel Booking Web Application

## Objective
The primary goal of this project is to study and practice modern asynchronous web development using the FastAPI framework and SQLAlchemy by building a hotel booking web application.

## Tech Stack
- **Programming Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Task Queue**: Redis, Celery
- **Containerization**: Docker
- **CI/CD**: GitLab CI
- **Testing**: Pytest
- **SSL Certificates**: Certbot/Let's Encrypt

## Features
- **Authentication and Authorization**: Implemented using JWT tokens.
- **Hotel Management**: Add and edit hotels, rooms, and amenities.
- **Search and Filtering**: Search for hotels with filters and pagination.
- **Room Booking**: Check room availability and make bookings.
- **Background Tasks**: 
  - Sending notifications.
  - Handling image uploads.
  - Powered by Celery and Redis.
- **Response Caching**: Optimized using Redis.

## Implementation
- Backend is developed using FastAPI and covered with integration tests.
- Clear separation of the business logic layer from FastAPI and the database.
- Provides a fully functional REST API.
- Exception handling ensures the application returns appropriate responses.

## Design Patterns
- **Repository Pattern**: For data abstraction.
- **Data Mapper Pattern**: To map database entities.
- **DTO (Data Transfer Object)**: For data validation and transformation.

## CI/CD Pipeline
- Automated processes configured in GitLab CI for testing and deployment.
- CI pipeline runs:
  - Unit and integration tests using **Pytest**.
  - Code linting using **ruff**.
  - Type checking with **pyright**.
- Fully typed Python code.

## Docker

#### Create Docker Network
```bash
docker network create myNetwork
```

#### DB
```bash
docker run --name booking_db \
    -p 5432:5432 \
    -e POSTGRES_USER=... \
    -e POSTGRES_PASSWORD=... \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16-bookworm
```

#### Redis
```bash
docker run --name booking_cache \
    -p 6379:6379 \
    --network=myNetwork \
    -d redis:7.4
```

#### NGINX
```bash
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=myNetwork \
    --rm -p 443:443 -d nginx
```
## Gitlab Runner

#### Run
```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```

#### Register runner
```bash
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register
```

#### Update config
`nano /srv/gitlab-runner/config/config.toml`
or
`vim /srv/gitlab-runner/config/config.toml`

Change `volumes = ["/cache"]` to
```toml
volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
```

#### Solving other issues
```bash
sudo groupadd docker
sudo usermod -aG docker $(whoami)
sudo service docker start
```
