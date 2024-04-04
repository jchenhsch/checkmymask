# Use the official Anaconda base image
FROM continuumio/anaconda3:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install libwebp
RUN apt-get update && \
    apt-get install -y libwebp-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install libjpeg-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libjpeg-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install opencv-python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libpng16-16 && \
    pip install --no-cache-dir opencv-python && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the gevent-websocket
RUN pip install gevent-websocket

# Expose ports 80 for HTTP and 443 for HTTPS
EXPOSE 8000
EXPOSE 443

# Run app.py when the container launches
CMD ["gunicorn","-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
