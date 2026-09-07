# VoiceScribe — Speech-to-Text Transcription Tool

A beginner-friendly **Artificial Intelligence intern project** that converts an uploaded audio recording into text. The project demonstrates a practical speech-recognition workflow with Python, `SpeechRecognition`, and a Streamlit web interface.

## Features

- Upload WAV, MP3, M4A, FLAC, AIFF, or OGG recordings.
- Select a recognition language.
- Convert non-WAV audio when FFmpeg is available.
- Transcribe speech with the Google Web Speech API.
- Display the transcript in the browser.
- Download the result as a `.txt` file.
- Clear error messages for unclear audio, network problems, and unsupported conversions.

## Tech stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Simple browser interface |
| SpeechRecognition | Speech-to-text API wrapper |
| Google Web Speech API | Default recognition engine |
| pydub + FFmpeg | Optional audio format conversion |

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate       # macOS/Linux
   # .venv\\Scripts\\activate      # Windows
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install **FFmpeg** if you want to process formats other than WAV. On Ubuntu/Debian:

   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## How the project works

The user uploads an audio file through Streamlit. WAV files are passed directly to `SpeechRecognition`; other supported formats are first converted to WAV with `pydub` and FFmpeg. The recognizer reads the audio, sends it to Google's Web Speech API, and returns the recognized text. The application stores the current transcript in Streamlit session state so it can be displayed and downloaded.

## Limitations

The default Google recognizer requires an internet connection, has service usage limits, and may be less accurate with noise, accents, or multiple speakers. The project is intended for learning and prototyping rather than sensitive or production transcription. Do not upload confidential recordings to a third-party recognition service.

## Suggested internship extensions

- Add timestamps by splitting long audio into segments.
- Add a history page with downloadable transcripts.
- Add audio waveform visualization.
- Add speaker diarization for multi-speaker recordings.
- Replace the online recognizer with an offline Whisper model.
- Add evaluation using Word Error Rate (WER) on a labeled test set.
- Build a small report comparing accuracy across languages and noise levels.

## Learning outcomes

By completing this project, an intern practices file handling, audio preprocessing, API-based AI integration, exception handling, user interface development, and responsible discussion of model limitations.
