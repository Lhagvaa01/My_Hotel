# Stage 1: Build the application
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app /app
COPY . .

EXPOSE 8000
CMD ["gunicorn", "My_Hotel_Django.wsgi:application", "--bind", "0.0.0.0:8000"]
