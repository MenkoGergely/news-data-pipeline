FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN npm install -r requirements.txt
COPY fetcher.py .
CMD ["python","fetcher.py"]

