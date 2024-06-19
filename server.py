from flask import Flask, request, jsonify, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
import os
import requests

app = Flask(__name__)
translator = Translator()

def extract_video_id(youtube_link):
    parsed_url = urlparse(youtube_link)
    query_params = parse_qs(parsed_url.query)
    
    # For URLs like https://www.youtube.com/watch?v=video_id
    if 'v' in query_params:
        return query_params['v'][0]
    
    # For URLs like https://youtu.be/video_id
    if parsed_url.path:
        path_parts = parsed_url.path.split('/')
        if len(path_parts) > 1:
            return path_parts[-1]
    
    return None

@app.route('/answer', methods=['GET'])
def get_answer():
    url = request.args.get('url')
    question = request.args.get('question')
    target_language = request.args.get('lang', 'en')  # Default to English if no language is specified
    
    video_id = extract_video_id(url)
    
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = get_transcript(video_id)
        translated_transcript = translate_transcript(transcript, target_language)
        
        # Generate speech audio file
        audio_filename = f"{video_id}_{target_language}.mp3"
        generate_text_to_speech(translated_transcript, audio_filename, target_language)
        
        answer = {
            "question": question,
            "translated_transcript": translated_transcript,
            "audio_url": request.host_url + f"audio/{audio_filename}"  # Full URL to access the audio file
        }
        return jsonify(answer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def translate_transcript(transcript, target_language):
    # Check if target_language is Hindi (code 'hi') or other supported languages
    if target_language != 'en':  # Only translate if target language is not English
        translated = translator.translate(transcript, dest=target_language)
        return translated.text
    else:
        return transcript  # Return original transcript if target language is English

def generate_text_to_speech(text, filename, target_language):
    tts = gTTS(text=text, lang=target_language, slow=False)
    tts.save(filename)

@app.route('/audio/<filename>', methods=['GET'])
def download_audio(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
