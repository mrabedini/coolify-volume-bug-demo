FROM python:3.11-alpine

WORKDIR /app

# Install a simple web server
RUN pip install --no-cache-dir flask

# Copy application files
COPY app.py /app/app.py
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
