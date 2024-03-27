FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY app ./app
CMD ["python", "-m", "app", "0:80"]
