FROM python:3.12.13-bookworm

WORKDIR /app

COPY scripts/requirements-docker.txt requirements.txt

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY scripts/ scripts/
COPY data/ data/

CMD ["python", "scripts/black_scholes.py"]