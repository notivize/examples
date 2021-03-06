from python:3.9.1
EXPOSE 8000

WORKDIR /notivize-diy
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY alembic.ini /
COPY diy.db.seed /diy.db
COPY ./alembic /alembic
COPY ./src /src
ENTRYPOINT ["uvicorn", "src.api:app", "--host", "0.0.0.0"]
