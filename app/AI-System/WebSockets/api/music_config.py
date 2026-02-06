from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class MusicGenerationMode(Enum):
    MUSIC_GENERATION_MODE_UNSPECIFIED = "MUSIC_GENERATION_MODE_UNSPECIFIED"
    QUALITY = "QUALITY"
    DIVERSITY = "DIVERSITY"
    VOCALIZATION = "VOCALIZATION"

class MusicScale(Enum):
    SCALE_UNSPECIFIED = "SCALE_UNSPECIFIED"
    C_MAJOR_A_MINOR = "C_MAJOR_A_MINOR"
    D_FLAT_MAJOR_B_FLAT_MINOR = "D_FLAT_MAJOR_B_FLAT_MINOR"
    D_MAJOR_B_MINOR = "D_MAJOR_B_MINOR"
    E_FLAT_MAJOR_C_MINOR = "E_FLAT_MAJOR_C_MINOR"
    E_MAJOR_D_FLAT_MINOR = "E_MAJOR_D_FLAT_MINOR"
    F_MAJOR_D_MINOR = "F_MAJOR_D_MINOR"
    G_FLAT_MAJOR_E_FLAT_MINOR = "G_FLAT_MAJOR_E_FLAT_MINOR"
    G_MAJOR_E_MINOR = "G_MAJOR_E_MINOR"
    A_FLAT_MAJOR_F_MINOR = "A_FLAT_MAJOR_F_MINOR"
    A_MAJOR_G_FLAT_MINOR = "A_MAJOR_G_FLAT_MINOR"
    B_FLAT_MAJOR_G_MINOR = "B_FLAT_MAJOR_G_MINOR"
    B_MAJOR_A_FLAT_MINOR = "B_MAJOR_A_FLAT_MINOR"

class PlaybackControl(Enum):
    PLAY = "PLAY"
    PAUSE = "PAUSE"
    STOP = "STOP"
    RESET_CONTEXT = "RESET_CONTEXT"

@dataclass
class WeightedPrompt:
    text: str
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "weight": self.weight
        }

@dataclass
class MusicGenerationConfig:
    temperature: float = 1.1        # 0.0 to 3.0
    topK: int = 40                  # 1 to 1000
    guidance: float = 4.0           # 0.0 to 6.0
    bpm: int = 120                  # 60 to 200
    density: float = 0.5            # 0.0 to 1.0
    brightness: float = 0.5         # 0.0 to 1.0
    muteBass: bool = False
    muteDrums: bool = False
    onlyBassAndDrums: bool = False
    scale: str = MusicScale.SCALE_UNSPECIFIED.value
    musicGenerationMode: str = MusicGenerationMode.QUALITY.value

    def to_dict(self) -> Dict[str, Any]:
        # Filter out default/unspecified values to keep payload clean if needed,
        # or send everything. For now, sending relevant fields.
        return {
            "temperature": self.temperature,
            "topK": self.topK,
            "guidance": self.guidance,
            "bpm": self.bpm,
            "density": self.density,
            "brightness": self.brightness,
            "muteBass": self.muteBass,
            "muteDrums": self.muteDrums,
            "onlyBassAndDrums": self.onlyBassAndDrums,
            "scale": self.scale,
            "musicGenerationMode": self.musicGenerationMode
        }

class MusicSessionConfig:
    def __init__(self, model: str = "models/lyria-realtime-exp"):
        self.model = model

    def get_setup_payload(self) -> Dict[str, Any]:
        return {
            "setup": {
                "model": self.model
            }
        }

    def get_client_content_payload(self, prompts: List[WeightedPrompt]) -> Dict[str, Any]:
        return {
            "client_content": {
                "weightedPrompts": [p.to_dict() for p in prompts]
            }
        }
    
    def get_generation_config_payload(self, config: MusicGenerationConfig) -> Dict[str, Any]:
        return {
            "music_generation_config": config.to_dict()
        }

    def get_playback_control_payload(self, control: PlaybackControl) -> Dict[str, Any]:
        return {
            "playback_control": control.value
        }
