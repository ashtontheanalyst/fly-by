FROM python:3.12-slim
WORKDIR /app

# git is needed for opensky-api
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy over and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose container port and run app
EXPOSE 8008
CMD ["python", "app.py"]