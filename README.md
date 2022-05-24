### Soal Test Tahap 2

#### Requirements
- Python3
- MongoDB
- Redis

#### Quick Setup

1. Clone this repository.
2. Create virtualenv
3. Install requirements from requirements.txt
4. Copy .env.example to .env `cp .env.example .env`
5. Set MONGO_URI, REDIS_URI and JWT_SECRET on .env
6. Run `flask run`
7. Run `celery -A celery_worker.celery worker --pool=solo --loglevel=info`
