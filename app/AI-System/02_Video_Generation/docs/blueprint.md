# Video Generation Blueprint 🎥

## Overview
This module transforms scripts or static images into dynamic video content. It utilizes **Gemini** for scene direction and advanced video models for rendering.

## Architecture

### 1. Script-to-Scene (Gemini 1.5 Pro)
-   **Input**: Music Video Script or Song Lyrics.
-   **Process**: Gemini breaks the text into a "Shot List" with camera angles, lighting, and movement descriptions.
-   **Output**: JSON list of prompts for each scene.

### 2. Image-to-Video (I2V) & Text-to-Video
-   **Core Model**: **Veo 3.1** (via `google-genai` SDK).
-   **Capabilities**:
    -   **Resolution**: 720p, 1080p, 4k.
    -   **Aspect Ratio**: 16:9 (Landscape), 9:16 (Portrait).
    -   **Input**: Text Prompts, Reference Images (Nano Banana), First/Last Frames.

### 3. Video Intelligence (Analysis)
-   **Core Model**: **Gemini 1.5 Pro** / **Gemini 2.0 Flash**.
-   **Capabilities**:
    -   Deep video understanding (visual + audio).
    -   QA (Questions & Answers) about video content.
    -   Extraction of tags, summaries, and descriptions.

## Directory Usage
-   `data/storyboards/`: Initial sketches or keyframes.
-   `data/clips/`: Rendered MP4 clips.
-   `flows/veo_cinema.py`: Video Generation Workflow.
-   `flows/analyze_scene.py`: Video Analysis Workflow.

## Workflow Example (Veo Cinema)
1.  **Director Mode**: "Cinematic drone shot..." -> Veo 3.1 -> 4K Video.
2.  **Animate Mode**: Nano Banana Image -> Veo 3.1 -> Animated Video.

## Workflow Example (Intelligence)
1.  **Input**: generated video `veo_direct.mp4`.
2.  **Prompt**: "Write a catchy Instagram caption for this."
3.  **Result**: "✨ Dive into the neon abyss! #Cyberpunk #4K"
