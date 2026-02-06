# Image Generation Blueprint 🖼️

## Overview
This module handles the creation of high-quality static assets (Album Covers, Merch Designs, Artist Avatars) using a hybrid **Gemini + Generative Model** workflow.

## Architecture

### 1. Concept Expansion (Gemini 1.5 Pro)
-   **Input**: Simple user concept (e.g., "Sad robot in rain").
-   **Process**: usage of `google_studio_manager.py` to act as a "Prompt Engineer".
-   **Output**: Detailed, stylistic prompt (e.g., "Cinematic shot of a rusted robot sitting on a neon street, heavy rain, cyberpunk aesthetic, 8k resolution, melancholic atmosphere").

### 2. Generation (Inference)
-   **Local Model**: Stable Diffusion XL (SDXL) via Automatic1111/ComfyUI API.
-   **Cloud Model**: Midjourney (via external bridge) or DALL-E 3.
-   **Script**: `api/generate_image.py` (To be implemented).

## Directory Usage
-   `prompts/`: Store `.txt` files of successful prompt engineering sessions.
-   `data/raw/`: Reference images for Image-to-Image.
-   `data/processed/`: Final upscaled outputs.
-   `models/`: Store `.safetensors` checkpoints (e.g., `JuggernautXL`, `RealityVision`).

## Workflow Example
```json
{
  "user_input": "Cyberpunk Diva",
  "gemini_enhanced": "A futuristic pop scholar diva...",
  "model_config": {
    "steps": 30,
    "cfg": 7,
    "sampler": "DPM++ 2M Karras"
  }
  "model_config": {
    "steps": 30,
    "cfg": 7,
    "sampler": "DPM++ 2M Karras"
  }
}
```

## Vision Intelligence (Gemini 2.0+) 👁️
-   **API**: `api/image_intelligence.py`
-   **Capabilities**:
    -   **Object Detection**: Returns 2D bounding boxes (JSON).
    -   **Segmentation**: Returns pixel-perfect masks (Base64).
    -   **Visual Q&A**: Deep image analysis.
-   **Lab**: `flows/vision_lab.py` (Usage: `python vision_lab.py detect image.png`)
