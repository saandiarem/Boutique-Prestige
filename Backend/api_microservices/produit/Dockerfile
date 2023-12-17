FROM python:3.10.9-slim-bullseye

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6080

CMD ["python", "microservice_produit.py"]