TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📡</text></svg>">
    <title> HLS Stream Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .card-header {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            border-radius: 15px 15px 0 0 !important;
            padding: 1.5rem;
        }
        .form-control {
            border-radius: 10px;
            padding: 12px;
            border: 2px solid #e9ecef;
        }
        .form-control:focus {
            border-color: #2193b0;
            box-shadow: 0 0 0 0.2rem rgba(33, 147, 176, 0.25);
        }
        .btn {
            padding: 12px 25px;
            border-radius: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .btn-primary {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            border: none;
        }
        .btn-danger {
            background: linear-gradient(45deg, #cb2d3e, #ef473a);
            border: none;
        }
        .alert {
            border-radius: 10px;
            padding: 1.2rem;
        }
        .alert-success {
            background: linear-gradient(45deg, #43cea2, #185a9d);
            color: white;
            border: none;
        }
        .stream-url {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            word-break: break-all;
            margin-top: 10px;
        }
        .status-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
    </style>
</head>
<body class="d-flex align-items-center py-4">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header position-relative">
                        <h3 class="text-white mb-0">
                            <i class="fas fa-broadcast-tower me-2"></i>
                            HLS Stream Generator
                        </h3>
                        <span id="stream-status" class="status-badge bg-secondary text-white">
                            <i class="fas fa-circle me-1"></i>Idle
                        </span>
                    </div>
                    <div class="card-body p-4">

                    {% if error %}
                    <div class="alert mb-4" style="background: linear-gradient(45deg, #cb2d3e, #ef473a); color: white; border: none; border-radius: 10px; padding: 1.2rem;">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-exclamation-circle me-2"></i>
                            <h5 class="mb-0">{{ error }}</h5>
                        </div>
                    </div>
                    {% endif %}
              
                        <form method="post" class="mb-4">
                            <div class="mb-4">
                                <label for="video_url" class="form-label h6">
                                    <i class="fas fa-link me-2"></i>Video URL
                                </label>
                                <input type="url" class="form-control form-control-lg" 
                                       id="video_url" name="video_url" 
                                       placeholder="Enter video URL (MP4)" required>
                            </div>
                            
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-play me-2"></i>Generate Stream
                                </button>
                                <button type="button" id="stop-stream" class="btn btn-danger">
                                    <i class="fas fa-stop me-2"></i>Stop Stream
                                </button>
                            </div>
                        </form>

                        {% if stream_url %}
                        <div class="mt-4">
                            <div class="alert alert-success">
                                <h5 class="mb-3">
                                    <i class="fas fa-check-circle me-2"></i>
                                    Your Stream URL
                                </h5>
                                <div class="stream-url">{{ stream_url }}</div>
                                <small class="d-block mt-2">
                                    <i class="fas fa-video me-2"></i>
                                    Currently playing: {{ current_video_url }}
                                </small>
                                <small class="d-block mt-2">
                                    <i class="fas fa-redo me-2"></i>
                                    Playing 1 time(s)
                                </small>
                                <small class="d-block mt-3">
                                    <i class="fas fa-info-circle me-2"></i>
                                    Use this URL in your media player
                                </small>
                            </div>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const stopButton = document.getElementById("stop-stream");
            const statusBadge = document.getElementById("stream-status");

            if ("{{ stream_url }}") {
                statusBadge.className = "status-badge bg-success text-white";
                statusBadge.innerHTML = '<i class="fas fa-circle me-1"></i>Streaming';
            }

            stopButton.addEventListener("click", () => {
                fetch("/stop-stream", {method: "POST"})
                    .then(response => response.json())
                    .then(data => {
                        statusBadge.className = "status-badge bg-secondary text-white";
                        statusBadge.innerHTML = '<i class="fas fa-circle me-1"></i>Stopped';
                    });
            });
        });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

from flask import Flask, request, render_template_string, send_from_directory, jsonify
import subprocess
import os
import tempfile
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

UPLOAD_FOLDER = tempfile.gettempdir()
streaming_active = {"value": True}
current_stream = {"ts_file": None, "duration": None, "current_video_url": None}

def create_single_chunk(video_url):
    try:
        # Convert the entire video into a single .ts chunk
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video_url,
            "-c:v", "copy",  # Copy video codec
            "-c:a", "copy",  # Copy audio codec
            "-bsf:v", "h264_mp4toannexb",  # Necessary for mpegts format
            "-f", "mpegts",  # Output format mpegts (Transport Stream)
            os.path.join(UPLOAD_FOLDER, "chunk.ts")  # Output file
        ]

        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        process.wait()
        logger.info("Single TS chunk created.")
    except Exception as e:
        logger.error(f"Error processing video for single chunk: {e}")

def create_playlist_for_single_chunk():
    try:
        # Create a simple playlist that references the single chunk
        playlist_content = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-ALLOW-CACHE:NO
#EXTINF:10,
chunk.ts
#EXT-X-ENDLIST
"""
        with open(os.path.join(UPLOAD_FOLDER, "stream.m3u8"), "w") as f:
            f.write(playlist_content)
        logger.info("Playlist created for single chunk.")
    except Exception as e:
        logger.error(f"Error creating playlist: {e}")

##########################################
@app.route("/", methods=["GET", "POST"])
def index():
    stream_url = None

    if request.method == "POST":
        if os.path.exists(os.path.join(UPLOAD_FOLDER, "chunk.ts")):
            # Return current stream info with error message
            return render_template_string(TEMPLATE, 
                error="Please stop the current stream before starting a new one.",
                stream_url=f"https://{request.host}/stream/stream.m3u8",
                current_video_url=current_stream["current_video_url"])
            
        video_url = request.form["video_url"]
        current_stream["current_video_url"] = video_url

        try:
            create_single_chunk(video_url)
            create_playlist_for_single_chunk()
            stream_url = f"https://{request.host}/stream/stream.m3u8"
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return render_template_string(TEMPLATE, error=str(e))

    return render_template_string(TEMPLATE, 
                                stream_url=stream_url if os.path.exists(os.path.join(UPLOAD_FOLDER, "chunk.ts")) else None, 
                                current_video_url=current_stream.get("current_video_url") if os.path.exists(os.path.join(UPLOAD_FOLDER, "chunk.ts")) else None)
##########################################

@app.route("/stop-stream", methods=["POST"])
def stop_stream():
    global streaming_active
    streaming_active["value"] = False
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, "stream.m3u8"))
        os.remove(os.path.join(UPLOAD_FOLDER, "chunk.ts"))
    except:
        pass
    return jsonify({"status": "stopped"})

@app.route("/stream/<path:filename>")
def serve_stream(filename):
    try:
        response = send_from_directory(UPLOAD_FOLDER, filename.split('?')[0])
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Cache-Control"] = "no-cache"
        return response
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
