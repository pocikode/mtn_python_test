import dotenv
from app import create_app

dotenv.load_dotenv()

app = create_app()
app.app_context().push()

from app import celery