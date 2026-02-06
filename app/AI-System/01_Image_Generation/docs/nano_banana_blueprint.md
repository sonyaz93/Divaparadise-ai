# Nano Banana Workflow 🍌

## Overview
This workflow implements a "Rapid Prototyping" approach to AI image generation, inspired by Google AI Studio's best practices. It balances speed and cost by using lightweight models for iteration and heavy models for final production.

## Models Used
1.  **Drafting**: `gemini-2.5-flash-image`
    -   **Strengths**: Extremely fast, low latency, good for composition checks.
    -   **Usage**: Generates 4 initial variations of the concept.
2.  **Production**: `gemini-3-pro-image-preview`
    -   **Strengths**: Maximum detail, complex lighting, photorealism.
    -   **Usage**: Takes the selected draft and renders the final high-resolution asset.

## Workflow Steps
1.  **Ideation**: User inputs a raw concept (e.g., "Neon Banana").
2.  **Flash Phase**: System generates 4 quick sketches using `gemini-2.5-flash-image`.
3.  **Selection**: User picks the best composition (e.g., Var #2).
4.  **Refinement**: `google_studio_manager` expands the prompt for that specific variation.
5.  **Pro Phase**: System generates the final image using `gemini-3-pro-image-preview`.

## Script
Run the workflow using:
```bash
python AI-System/01_Image_Generation/flows/nano_banana.py "Your Concept"
```

## Folder Structure
-   **Script**: `flows/nano_banana.py`
-   **Outputs**: `data/outputs/`
