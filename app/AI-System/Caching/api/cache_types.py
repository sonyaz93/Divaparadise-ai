from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
import datetime

@dataclass
class CachedContentConfig:
    """
    Configuration for creating a Content Cache.
    """
    model: str
    contents: List[Dict[str, Any]] # Standard Content objects
    ttl_seconds: Optional[int] = None
    expire_time: Optional[str] = None # RFC 3339 timestamp
    display_name: Optional[str] = None
    system_instruction: Optional[Dict[str, Any]] = None # Content object

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "model": self.model,
            "contents": self.contents
        }
        
        if self.ttl_seconds:
            data["ttl"] = f"{self.ttl_seconds}s"
        
        if self.expire_time:
            data["expireTime"] = self.expire_time
            
        if self.display_name:
            data["displayName"] = self.display_name
            
        if self.system_instruction:
            data["systemInstruction"] = self.system_instruction
            
        return data

@dataclass
class UpdateCacheConfig:
    """
    Configuration for updating a Content Cache.
    """
    ttl_seconds: Optional[int] = None
    expire_time: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.ttl_seconds:
            data["ttl"] = f"{self.ttl_seconds}s"
        if self.expire_time:
            data["expireTime"] = self.expire_time
        return data
