# Start with a Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install required dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    ca-certificates \
    libx11-6 \
    libxcomposite1 \
    libxrandr2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libpango-1.0-0 \
    libvulkan1 \
    libasound2 \
    xdg-utils \
    fonts-liberation \
    && apt-get clean

# Install specific version of Google Chrome (113.0.5672.64)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_113.0.5672.64-1_amd64.deb \
    && dpkg -i google-chrome-stable_113.0.5672.64-1_amd64.deb \
    && apt-get install -f -y \
    && rm google-chrome-stable_113.0.5672.64-1_amd64.deb

# Install matching version of ChromeDriver for version 113.0.5672.64
RUN wget https://storage.googleapis.com/chrome-for-testing-public/113.0.5672.64/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && rm -rf chromedriver-linux64 chromedriver-linux64.zip

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
