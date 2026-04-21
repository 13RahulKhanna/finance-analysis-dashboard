FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline/ ./pipeline/
COPY llm/ ./llm/
COPY main.py run.py ./
COPY data.csv ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
