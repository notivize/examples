from python:3.9.1
EXPOSE 8000

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY ./src ./src
COPY diy.db.seed diy.db
ENTRYPOINT ["uvicorn", "src.api:app", "--host", "0.0.0.0"]
