# HLS Stream Generator

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Docker](https://img.shields.io/badge/Docker-20.10-2496ED?style=for-the-badge&logo=docker&logoColor=white) 
![Render](https://img.shields.io/badge/Render-Deployed-4CAF50?style=for-the-badge&logo=render&logoColor=white) 
![MIT License](https://img.shields.io/badge/License-MIT-FFEB3B?style=for-the-badge&logo=open-source-initiative&logoColor=303030) 
![VLC](https://img.shields.io/badge/VLC-Media_Player-E95420?style=for-the-badge&logo=vlc&logoColor=white)

![image](https://github.com/user-attachments/assets/a415ac8c-739e-4253-bd1b-4788203b9dec)




## Overview
HLS Stream Generator is a Flask-based application that generates HTTP Live Streaming (HLS) URLs from video URLs. It uses FFmpeg to create video chunks and playlists for seamless video streaming.

## Features
- Convert video URLs (MP4) to HLS streams.
- Generate M3U8 playlists and TS chunks.
- Simple, intuitive web interface for generating and stopping streams.
- Deployed and accessible at [https://hlstest.onrender.com](https://hlstest.onrender.com).

## Model Details
- **Framework:** Flask 2.3.3
- **Video Processing:** FFmpeg
- **Hosting:** Render
- **Containerization:** Docker

## How It Works
1. Input a video URL (MP4) in the web interface.
2. The server processes the video and generates HLS-compatible chunks and playlists.
3. The generated stream URL can be used in media players supporting HLS.
4. Streams can be stopped directly from the interface.

## Usage
### Using Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/SanshruthR/mock-hls-server.git
   cd mock-hls-server
   ```
2. Build the Docker image:
   ```bash
   docker build -t hls-stream-generator .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 5000:5000 hls-stream-generator
   ```
4. Access the application at `http://localhost:5000`.

### Without Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/SanshruthR/mock-hls-server.git
   cd mock-hls-server
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the application at `http://localhost:5000`.

## Deployment
The application is deployed on Render and can be accessed at [https://hlstest.onrender.com](https://hlstest.onrender.com).

## License
This project is licensed under the MIT License.

---

