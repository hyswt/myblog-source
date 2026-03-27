FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY cms/requirements.txt /app/cms/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/cms/requirements.txt

COPY . /app
WORKDIR /app/cms

RUN chmod +x start.sh

EXPOSE 8000

CMD ["bash", "start.sh"]
