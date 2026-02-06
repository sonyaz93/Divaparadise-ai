from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class BatchState(Enum):
    STATE_UNSPECIFIED = "BATCH_STATE_UNSPECIFIED"
    PENDING = "BATCH_STATE_PENDING"
    RUNNING = "BATCH_STATE_RUNNING"
    SUCCEEDED = "BATCH_STATE_SUCCEEDED"
    FAILED = "BATCH_STATE_FAILED"
    CANCELLED = "BATCH_STATE_CANCELLED"
    EXPIRED = "BATCH_STATE_EXPIRED"

@dataclass
class GenerateContentRequest:
    model: str
    contents: List[Dict[str, Any]] # Content objects
    generation_config: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "model": self.model,
            "contents": self.contents
        }
        if self.generation_config:
            data["generation_config"] = self.generation_config
        return data

@dataclass
class InlinedRequest:
    request: GenerateContentRequest
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request": self.request.to_dict()
        }

@dataclass
class BatchRequestInput:
    """
    Helper to construct the batch input config.
    """
    requests: List[GenerateContentRequest]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "requests": {
                "requests": [InlinedRequest(r).to_dict() for r in self.requests]
            }
        }
