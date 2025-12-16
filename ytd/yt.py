from flask import Flask, request, send_file, render_template_string
import subprocess
import os
import uuid

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Downloader</title>
</head>
<body>
    <h1>Video Downloader</h1>

    <form method="POST">
        <label>Video URL:</label><br>
        <input type="text" name="url" required><br><br>

        <label>Select Format:</label><br>
        <select name="format">
            <option value="mp4">Video (MP4)</option>
            <option value="mp3">Audio (MP3)</option>
        </select><br><br>

        <label>Select Quality:</label><br>
        <select name="quality">
            <option value="best">Best</option>
            <option value="720">720p</option>
            <option value="480">480p</option>
            <option value="360">360p</option>
            <option value="240">240p</option>
        </select><br><br>

        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # Clean URL (remove ?si= etc.)
        url = url.split("?")[0]

        format_type = request.form["format"]
        quality = request.form["quality"]

        uid = str(uuid.uuid4())
        output_template = f"{uid}.%(ext)s"

        # yt-dlp base command with fallback options
        cmd = [
            "yt-dlp",
            "--no-check-certificate",
            "--no-warnings",
            "--ignore-errors",
            "-o", output_template
        ]

        # MP3 download
        if format_type == "mp3":
            cmd += ["-x", "--audio-format", "mp3"]

        # MP4 download
        else:
            if quality == "best":
                cmd += ["-f", "bv*+ba/b"]
            else:
                cmd += ["-f", f"bv*[height<={quality}]+ba/b[height<={quality}]"]

        cmd.append(url)

        try:
            subprocess.run(cmd, check=True)

            # Find downloaded file
            for f in os.listdir():
                if f.startswith(uid):
                    return send_file(f, as_attachment=True)

            return "Download failed"

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template_string(HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
