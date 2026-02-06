# Lip Sync Generation Blueprint 🗣️

## Overview
The final stage of production. This module synchronizes a generated video character's lip movements with a generated audio track.

## Architecture

### 1. Input Alignment
-   **Video Source**: From `02_Video_Generation` (Must contain a clear face).
-   **Audio Source**: From `03_Audio_Generation` (Vocals only preferred).

### 2. Deep Fake / Sync Process
-   **Core Model**: **Wav2Lip** (and its variants like Wav2Lip-GAN).
-   **Refinement**: **CodeFormer** or **GFPGAN** to fix the "blurry mouth" artifact common in Wav2Lip.

## Directory Usage
-   `models/checkpoints/`: `wav2lip.pth`, `wav2lip_gan.pth`.
-   `data/inputs/`: Paired Video + Audio files.
-   `data/outputs/`: Final synchronized MP4s.

## Workflow Example
1.  **Select**: `video_scene_01.mp4` + `audio_verse_01.wav`.
2.  **Process**: Run `inference.py` (Wav2Lip).
3.  **Post-Process**: Run CodeFormer to sharpen the face.
4.  **Result**: A character singing the lyrics perfectly.
