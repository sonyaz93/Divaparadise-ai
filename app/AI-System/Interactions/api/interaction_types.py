from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class InteractionRole(Enum):
    USER = "user"
    MODEL = "model"

class InteractionStatus(Enum):
    IN_PROGRESS = "in_progress"
    REQUIRES_ACTION = "requires_action"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ToolChoiceType(Enum):
    AUTO = "auto"
    ANY = "any"
    NONE = "none"
    VALIDATED = "validated"

@dataclass
class AgentOption:
    DEEP_RESEARCH = "deep-research-pro-preview-12-2025"

@dataclass
class ModelOption:
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_3_PRO = "gemini-3-pro-preview"
    GEMINI_3_FLASH = "gemini-3-flash-preview"

@dataclass
class DeepResearchAgentConfig:
    type: str = "deep-research"
    thinking_summaries: str = "auto" # or "none"

@dataclass
class InteractionInput:
    """
    Helper to construct the input payload.
    Supports text, but can be extended for images/files.
    """
    text: str
    
    def to_dict(self) -> Dict[str, Any]:
        # Simple text input for now. 
        # The API accepts: input: Content | Content[] | Turn[] | string
        # We will use the string or Content format.
        return {
            "role": "user",
            "content": [{"type": "text", "text": self.text}]
        }

@dataclass
class InteractionConfig:
    model: Optional[str] = None
    agent: Optional[str] = None
    agent_config: Optional[Any] = None
    tools: Optional[List[Dict]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        payload = {}
        if self.model:
            payload["model"] = self.model
        if self.agent:
            payload["agent"] = self.agent
            if self.agent_config:
                payload["agent_config"] = self.agent_config.__dict__
        if self.tools:
            payload["tools"] = self.tools
        return payload
