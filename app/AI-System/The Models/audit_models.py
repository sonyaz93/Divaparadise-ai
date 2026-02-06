import json
import os
import sys

def audit():
    print("=== MODEL SYSTEMS AUDIT ===")
    
    # 1. Check Manifest
    manifest_path = "model_manifest.json"
    if not os.path.exists(manifest_path):
        print("[FAIL] model_manifest.json missing!")
        return
    
    with open(manifest_path, "r") as f:
        data = json.load(f)
        
    print(f"[OK] Manifest loaded (Ver: {data.get('schema_version')})")
    
    # 2. Check Local Weights
    local_models = data.get("system_models", {}).get("local_models", {})
    for name, info in local_models.items():
        path = info.get("path")
        if path:
            if os.path.exists(path):
                print(f"[OK] Local Model '{name}': Found ({path})")
            else:
                req = "REQUIRED" if info.get("required") else "OPTIONAL"
                status = "[FAIL]" if info.get("required") else "[WARN]"
                print(f"{status} Local Model '{name}': Missing ({path}) - {req}")

    # 3. Check System Prompts
    prompts_dir = "system_prompts"
    if os.path.exists(prompts_dir):
        files = os.listdir(prompts_dir)
        print(f"[OK] System Prompts: {len(files)} found.")
    else:
        print("[WARN] system_prompts directory missing.")

    print("\nAudit Complete.")

if __name__ == "__main__":
    audit()
