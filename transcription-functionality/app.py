from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from src.transcription import load_whisper_model, transcribe_audio
from src.video_to_audio import extract_audio_from_video
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model = load_whisper_model()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    video_file = request.files['file']
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)
    
    audio_path = os.path.join('uploads', os.path.splitext(video_file.filename)[0] + '.mp3')
    extract_audio_from_video(video_path, audio_path)
    
    transcription = transcribe_audio(model, audio_path)
    
    transcription_file_path = os.path.join('uploads', os.path.splitext(video_file.filename)[0] + '_transcription.txt')
    with open(transcription_file_path, 'w') as f:
        for line in transcription:
            f.write(line + '\n')
    
    os.remove(video_path)
    os.remove(audio_path)
    
    if os.path.exists(transcription_file_path):
        return send_file(transcription_file_path, as_attachment=True)
    else:
        return jsonify({"error": "Transcription file not found"}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
