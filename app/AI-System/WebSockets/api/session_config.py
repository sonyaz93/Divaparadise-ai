import os
from typing import List, Dict, Any, Optional

class SessionConfig:
    """
    Manages the configuration for the Gemini Live API session via WebSockets.
    Defines model, generation config, system instructions, and tools.
    """
    def __init__(
        self,
        model_name: str = "models/gemini-2.0-flash-exp",
        system_instruction: str = "You are a helpful AI assistant.",
        tools: Optional[List[Dict]] = None,
        generation_config: Optional[Dict] = None
    ):
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.tools = tools or []
        
        # Default Generation Config
        self.generation_config = generation_config or {
            "responseModalities": ["AUDIO"],  # Default to Audio response for Live API
            "candidateCount": 1,
            "maxOutputTokens": 2048,
            "temperature": 0.7,
            "topP": 0.95,
        }

    def get_setup_payload(self) -> Dict[str, Any]:
        """
        Constructs the BidiGenerateContentSetup payload for the initial handshake.
        """
        payload = {
            "setup": {
                "model": self.model_name,
                "generationConfig": self.generation_config,
                "systemInstruction": {
                    "parts": [{"text": self.system_instruction}]
                }
            }
        }
        
        if self.tools:
            payload["setup"]["tools"] = self.tools
            
        return payload

    def update_system_instruction(self, new_instruction: str):
        self.system_instruction = new_instruction

    def set_response_modality(self, modality: str):
        """
        Set response modality: "AUDIO" or "TEXT".
        """
        if modality.upper() in ["AUDIO", "TEXT"]:
            self.generation_config["responseModalities"] = [modality.upper()]
