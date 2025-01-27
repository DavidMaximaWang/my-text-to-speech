from flask import Flask, request, jsonify, send_file
from google.cloud import texttospeech
from io import BytesIO
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all domains (you can restrict this if needed)
CORS(app)

# Initialize the Google Text-to-Speech client
client = texttospeech.TextToSpeechClient()

@app.route('/synthesize', methods=['POST'])
def synthesize_text():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    audio_stream = BytesIO(response.audio_content)
    audio_stream.seek(0)

    return send_file(audio_stream, mimetype="audio/mp3", as_attachment=True, download_name="output.mp3")

if __name__ == '__main__':
    app.run(debug=True)
