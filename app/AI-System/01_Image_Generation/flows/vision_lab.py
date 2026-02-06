import sys
import os
import json
import base64
import io
import numpy as np
from PIL import Image, ImageDraw

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from image_intelligence import ImageIntelligence

def draw_boxes(image_path, boxes, output_path):
    """Draws bounding boxes on the image."""
    try:
        im = Image.open(image_path)
        draw = ImageDraw.Draw(im)
        width, height = im.size
        
        for item in boxes:
            box = item.get("box_2d")
            label = item.get("label", "Object")
            
            if box:
                # Gemini returns [ymin, xmin, ymax, xmax] 0-1000
                ymin, xmin, ymax, xmax = box
                
                # Convert to absolute
                abs_y1 = int(ymin / 1000 * height)
                abs_x1 = int(xmin / 1000 * width)
                abs_y2 = int(ymax / 1000 * height)
                abs_x2 = int(xmax / 1000 * width)
                
                # Draw Box
                draw.rectangle([abs_x1, abs_y1, abs_x2, abs_y2], outline="red", width=3)
                draw.text((abs_x1, abs_y1), label, fill="red")
        
        im.save(output_path)
        print(f"[SAVED] Detection result: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Drawing failed: {e}")

def main():
    print("[INFO] Initializing Vision Lab 👁️...")
    
    if len(sys.argv) < 3:
        print("Usage: python vision_lab.py [detect|segment] <image_path>")
        return

    mode = sys.argv[1]
    image_path = sys.argv[2]
    
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    # Initialize API (Using Gemini 2.0 Flash for speed/vision)
    intel = ImageIntelligence(model_name="gemini-2.0-flash-exp")
    
    if mode == "detect":
        print(f"\n--- DETECTING OBJECTS in {image_path} ---")
        results = intel.detect_objects(image_path)
        print(json.dumps(results, indent=2))
        
        # Visualize
        output_filename = f"detected_{os.path.basename(image_path)}"
        output_path = os.path.join(os.path.dirname(image_path), output_filename)
        draw_boxes(image_path, results, output_path)

    elif mode == "segment":
        print(f"\n--- SEGMENTING OBJECTS in {image_path} ---")
        print("Note: Implementation relies on 'mask' field in JSON.")
        results = intel.segment_objects(image_path)
        # Visualization logic for masks would go here (decoding base64, overlays)
        # Simplified for this lab:
        print(f"Found {len(results)} segments.")

if __name__ == "__main__":
    main()
