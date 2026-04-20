FROM python:3.10-slim

WORKDIR /app

COPY flask_app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data

VOLUME ["/data"]

EXPOSE 5000

CMD ["python", "app.py"]
