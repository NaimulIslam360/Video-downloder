# Single-file Flask Video -> Audio (MP3) Extractor

from flask import Flask, render_template_string, request, send_file
import os, uuid, subprocess

app = Flask(__name__)

UPLOAD = 'uploads'
OUTPUT = 'outputs'
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<body>
<h2>Video to Audio</h2>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="video" required>
<button type="submit">Extract</button>
</form>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        v = request.files['video']
        uid = str(uuid.uuid4())
        vpath = os.path.join(UPLOAD, uid + v.filename)
        apath = os.path.join(OUTPUT, uid + '.mp3')

        v.save(vpath)
        subprocess.run(['ffmpeg','-i',vpath,'-vn',apath])

        return send_file(apath, as_attachment=True)

    return render_template_string(HTML)

app.run(debug=True)