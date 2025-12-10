
# 1) Use lightweight Python base image
FROM python:3.11-slim

# 2) Set working directory
WORKDIR /app

# 3) Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy all project files (models + code + HTML)
COPY . .

# 5) Expose port (FastAPI default)
EXPOSE 8000

# 6) Run flaskAPI 
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
