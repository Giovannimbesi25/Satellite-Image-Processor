FROM python:3.9

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/src

CMD ["python", "app.py"]
