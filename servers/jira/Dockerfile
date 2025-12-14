FROM mcp-base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY servers/jira /app
COPY shared /app/shared

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]
