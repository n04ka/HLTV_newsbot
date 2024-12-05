FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80:80

CMD ["fastapi", "run", "src/main.py", "--port", "80"]