# The Models 🧠

This directory serves as the CENTRAL REGISTRY for all AI models, system prompts, and local weights used in the Divaparadises AI System.

## Structure

-   `model_manifest.json`: The "Source of Truth". Lists all active models (both API and Local) and their configurations.
-   `system_prompts/`: Contains `.txt` files with distinct personas or system instructions (e.g., `cyberpunk_gm.txt`, `artist_bio_writer.txt`).
-   `weights/`: (GitIgnored) Local model binaries (e.g., `.pth`, `.safetensors`). **DO NOT COMMIT FILES HERE.**

## Usage

### Adding a System Prompt
1.  Create a new file in `system_prompts/` (e.g., `my_persona.txt`).
2.  Reference it in your code by loading it from this canonical path.

### Adding a Local Model
1.  Download the weights file.
2.  Place it in `weights/`.
3.  Update `model_manifest.json` under `local_models` to track it.

### Verifying Environment
Run the audit script to ensure you have everything needed:
```bash
python audit_models.py
```
