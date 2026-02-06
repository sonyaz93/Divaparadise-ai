# Audio Generation Blueprint 🎵

## Overview
This module handles the synthesis of music (instrumentals) and voice (TTS/Singing). It allows generic users to create "Demos" or backing tracks.

## Architecture

### 1. Composition (Gemini 1.5 Pro)
-   **Input**: Genre, Mood, Topic.
-   **Process**: Gemini writes lyrics (Verse/Chorus structure) and suggests chord progressions or stylistic tags.
-   **Output**: Meta-tags for the audio generator.

### 2. Sound Synthesis
-   **Voice (TTS)**:
    -   **ElevenLabs**: High-quality spoken word (Bios, intros).
    -   **RVC (Retrieval-based Voice Conversion)**: Converting a generic vocal to a specific "Diva" voice model.
-   **Music**:
    -   **MusicGen (Meta)**: Local/Cloud generation of 30s clips.
    -   **Suno AI**: Full song generation (via web bridge).

## Directory Usage
-   `data/voice_samples/`: 10-20s clean WAV files for RVC training.
-   `models/rvc/`: Voice models (.pth).
-   `data/outputs/`: Final MP3/WAV tracks.

## Workflow Example
-   **Input**: "Hyperpop sad song."
-   **Gemini**: Writes lyrics about "Digital tears."
-   **MusicGen**: Generates 120BPM synth backing loop.
-   **RVC**: Overlays user vocal with "CyberDiva" voice.

## Gemini Audio Studio 🎙️
-   **API**: `api/audio_client.py`
-   **Capabilities**:
    -   **TTS**: High-fidelity speech generation.
    -   **Multi-Speaker**: Conversations with distinct voices/personas.
    -   **Podcast Studio**: `flows/podcast_studio.py` (Script + Voice workflow).

## Audio Intelligence (Listening) 👂
-   **API**: `api/audio_analyzer.py`
-   **Capabilities**:
    -   **Transcription**: Timestamped Speech-to-Text.
    -   **Diarization**: Distinguishes distinct speakers.
    -   **Emotion**: Analyzes sentiment per segment.
-   **Lab**: `flows/transcription_lab.py` (Usage: `python transcription_lab.py audio.mp3`)
