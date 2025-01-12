FROM python:3.9-slim
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ffmpeg \
    libterm-readline-perl-perl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install Flask==2.3.3 psutil
WORKDIR /app
COPY app.py .
RUN mkdir -p /app/tmp
CMD ["python", "app.py"]
