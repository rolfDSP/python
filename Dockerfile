# Small official Python image, same Python version as the local venv.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

WORKDIR /app

# Install dependencies first so this layer is cached when only main.py changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Run as a non-root user; UID/GID default to 1000 so files in a mounted
# host folder belong to the normal host user.
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" app \
    && useradd -u "${UID}" -g app -M -s /usr/sbin/nologin app \
    && mkdir -p /data && chown app:app /data
USER app

VOLUME /data
EXPOSE 6060

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6060"]
