FROM python:3.11.5-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /resident_bot

COPY ./ /resident_bot/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot/main.py"]
