# Use a slim Python image to keep the build size small
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for Playwright and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements file and install the libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# If you use Playwright, you need to install the browser binaries
RUN playwright install-deps && playwright install chromium

# Copy the rest of your application code
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]