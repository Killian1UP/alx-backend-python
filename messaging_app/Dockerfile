# 1️⃣ Use base Python image
FROM python:3.10

# 2️⃣ Set environment variables to prevent Python buffering and save logs immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set work directory in the container
WORKDIR /app

# 4️⃣ Install system dependencies (optional but recommended for MySQL client)
RUN apt-get update && apt-get install -y \
    libmariadb-dev libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6️⃣ Copy the rest of the application code
COPY . /app/

# 7️⃣ Expose Django's default port -p
EXPOSE 8000

# 8️⃣ Default command to run Django (can be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

