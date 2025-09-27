FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY models/ models/
COPY app.py app.py

RUN ls --recursive .

EXPOSE 5000

CMD ["python", "app.py"]
