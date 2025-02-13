# Django + FastAPI Blockchain App

This is an example of an application where Django (for admin and ORM) and FastAPI (for API endpoints) work together.

## Functionality
- **Django Admin** (available at `/admin`)
- API endpoints for (Visit `/docs` for more detailed API documentation and testing):
  - User registrations (`POST /api/register`)
  - Login (`POST /api/login`)
  - List all providers (`GET /api/providers`)
  - Getting the list of blocks with filters and pagination (`GET /api/blocks?currency=ETH&provider=BlockChair&page=1&per_page=10`)
  - Retrieving block details by ID (`GET /api/blocks/{block_id}`)
  - Retrieving block details by currency name and block number (`GET /api/blocks/{currency_name}/{block_number}`)
- **Celery**: periodically (e.g. every minute, search for `CELERY_BEAT_SCHEDULE` inside `settings.py`) receives block data from external APIs (CoinMarketCap and BlockChair) and stores it in the database.

## How to start
- Install Docker and Docker Compose on your system if you do not have it.
- Run command:
    ```bash
    docker-compose up --build
    ```
### Open:
- FastAPI: [http://localhost:8000](http://localhost:8000) or even better here [http://localhost:8000/docs](http://localhost:8000/docs)
- Django Admin: [http://localhost:8000/admin](http://localhost:8000/admin)  
   To create `django superuser` run in your terminal:
    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

### To stop the project
Press `Ctrl+C` in your terminal and run command below to destroy all containers:
```bash
docker-compose down
