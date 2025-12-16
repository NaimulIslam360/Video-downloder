from flask import Flask, request, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ভিডিও ফাইল আপলোড করুন
        video_file = request.files['video']
        video_file.save('video.mp4')

        # অডিও এক্সট্রাক্ট করুন
        video = VideoFileClip('video.mp4')
        audio = video.audio
        audio.write_audiofile('audio.mp3')

        # অডিও ফাইল ডাউনলোড করুন
        return send_file('audio.mp3', as_attachment=True)

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="video">
        <input type="submit" value="অডিও এক্সট্রাক্ট করুন">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)