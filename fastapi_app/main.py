import os
import django
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.wsgi import get_wsgi_application

app = FastAPI(title="Django + FastAPI App")

django_app = get_wsgi_application()
app.mount("/admin", WSGIMiddleware(django_app))
app.mount(
    "/staticfiles",
    StaticFiles(directory="/blockchain_monitor/staticfiles"),
    name="staticfiles",
)

from .routes import router as api_router

app.include_router(api_router, prefix="/api")
