FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blockchain_monitor

COPY requirements.txt /blockchain_monitor/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /blockchain_monitor/

RUN apt-get update && apt-get install -y netcat-openbsd
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000"]