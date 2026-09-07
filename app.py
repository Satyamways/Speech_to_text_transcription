"""Speech-to-text transcription tool for an AI internship project."""

from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path

import speech_recognition as sr
import streamlit as st

try:
    from pydub import AudioSegment
except ImportError:  # pydub is optional for WAV-only usage
    AudioSegment = None


st.set_page_config(
    page_title="VoiceScribe | Speech-to-Text",
    page_icon="🎙️",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main { background: #f8fafc; }
    .block-container { max-width: 860px; padding-top: 3rem; }
    .hero { padding: 2rem; border-radius: 24px; background: linear-gradient(135deg, #172554, #2563eb); color: white; margin-bottom: 1.5rem; }
    .hero h1 { color: white; margin-bottom: .35rem; }
    .hero p { color: #dbeafe; font-size: 1.05rem; margin: 0; }
    .hint { color: #475569; font-size: .92rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🎙️ VoiceScribe</h1>
        <p>Convert an audio recording into text using Python speech recognition.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Project details")
    st.write("**AI Intern Project**")
    st.write("A simple demonstration of audio preprocessing, speech recognition, and a web UI.")
    st.divider()
    st.markdown("**How it works**")
    st.markdown("1. Upload an audio file\n2. Convert it to WAV if needed\n3. Send audio to the recognizer\n4. Display and download the transcript")
    st.caption("Recognition uses Google's public Web Speech API through the SpeechRecognition package. An internet connection is required for transcription.")

st.subheader("1. Upload an audio recording")
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a", "flac", "aiff", "aiff", "ogg"],
    help="WAV works out of the box. MP3/M4A/FLAC/OGG conversion requires pydub and FFmpeg.",
)

language = st.selectbox(
    "Recognition language",
    options=["en-US", "en-GB", "hi-IN", "es-ES", "fr-FR", "de-DE"],
    format_func=lambda code: {
        "en-US": "English (US)", "en-GB": "English (UK)", "hi-IN": "Hindi",
        "es-ES": "Spanish", "fr-FR": "French", "de-DE": "German",
    }[code],
)


def get_wav_bytes(file_name: str, file_bytes: bytes) -> bytes:
    """Return WAV bytes, converting common formats when pydub/FFmpeg are available."""
    suffix = Path(file_name).suffix.lower()
    if suffix == ".wav":
        return file_bytes
    if AudioSegment is None:
        raise RuntimeError("Install pydub and FFmpeg to convert non-WAV files.")
    try:
        audio = AudioSegment.from_file(io.BytesIO(file_bytes), format=suffix.lstrip("."))
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        return wav_buffer.getvalue()
    except Exception as exc:
        raise RuntimeError(f"Could not convert this audio file: {exc}") from exc


def transcribe(wav_bytes: bytes, recognition_language: str) -> str:
    """Transcribe WAV bytes with SpeechRecognition's Google recognizer."""
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(wav_bytes)
        temp_path = temp_file.name
    try:
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=recognition_language)
    finally:
        os.unlink(temp_path)


if uploaded_file:
    st.audio(uploaded_file)
    st.caption(f"Loaded: {uploaded_file.name} · {uploaded_file.size / 1024:.1f} KB")

    if st.button("Transcribe recording", type="primary", use_container_width=True):
        with st.spinner("Converting audio and recognizing speech…"):
            try:
                wav_data = get_wav_bytes(uploaded_file.name, uploaded_file.getvalue())
                transcript = transcribe(wav_data, language)
                st.session_state["transcript"] = transcript
            except sr.UnknownValueError:
                st.error("The speech could not be understood. Try a clearer recording with less background noise.")
            except sr.RequestError:
                st.error("The speech recognition service is unavailable. Check your internet connection and try again.")
            except Exception as exc:
                st.error(str(exc))

if st.session_state.get("transcript"):
    st.subheader("2. Transcript")
    transcript = st.session_state["transcript"]
    st.text_area("Recognized text", value=transcript, height=220, label_visibility="collapsed")
    st.download_button(
        "Download transcript (.txt)",
        data=transcript,
        file_name="transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.success(f"Transcription complete — {len(transcript.split())} words recognized.")
else:
    st.info("Upload a recording and click **Transcribe recording** to generate a transcript.")

st.divider()
st.markdown('<p class="hint">Tip: For best results, use a short, clear recording in a quiet environment.</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Streamlit runs this file with: streamlit run app.py
    pass


# Keep this file self-contained and beginner-friendly for internship review.
# Suggested next steps: add timestamps, speaker labels, and offline recognition with Whisper.
