#!/usr/bin/env python3
"""
Storage Manager for AI-Generated Content
Handles saving, organizing, and retrieving generated images, videos, and audio
"""

import os
import uuid
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import shutil
import requests
from PIL import Image
import io

class StorageManager:
    """Manages storage of AI-generated content"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent / "storage"
        self.images_path = self.base_path / "images"
        self.videos_path = self.base_path / "videos"
        self.audio_path = self.base_path / "audio"
        self.metadata_file = self.base_path / "metadata.json"
        
        # Create directories
        self._ensure_directories()
        
        # Load metadata
        self.metadata = self._load_metadata()
    
    def _ensure_directories(self):
        """Create storage directories if they don't exist"""
        for path in [self.images_path, self.videos_path, self.audio_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_metadata(self) -> Dict:
        """Load metadata from file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metadata: {e}")
        
        return {
            "images": {},
            "videos": {},
            "audio": {},
            "stats": {
                "total_images": 0,
                "total_videos": 0,
                "total_audio": 0,
                "created": datetime.now().isoformat()
            }
        }
    
    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving metadata: {e}")
    
    def _generate_filename(self, content_type: str, prompt: str, extension: str) -> str:
        """Generate unique filename based on content and timestamp"""
        # Create hash from prompt for consistency
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate unique ID
        unique_id = str(uuid.uuid4())[:8]
        
        return f"{content_type}_{timestamp}_{prompt_hash}_{unique_id}.{extension}"
    
    def save_image_from_url(self, url: str, prompt: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Download and save image from URL"""
        try:
            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                extension = 'jpg'
            elif 'png' in content_type:
                extension = 'png'
            elif 'webp' in content_type:
                extension = 'webp'
            else:
                extension = 'jpg'  # Default
            
            # Generate filename
            filename = self._generate_filename("image", prompt, extension)
            file_path = self.images_path / filename
            
            # Save image
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Create thumbnail
            thumbnail_path = self._create_thumbnail(file_path)
            
            # Prepare metadata
            image_metadata = {
                "id": str(uuid.uuid4()),
                "filename": filename,
                "original_url": url,
                "prompt": prompt,
                "file_path": str(file_path),
                "thumbnail_path": str(thumbnail_path) if thumbnail_path else None,
                "file_size": file_path.stat().st_size,
                "created_at": datetime.now().isoformat(),
                "content_type": content_type,
                "extension": extension,
                **(metadata or {})
            }
            
            # Add to metadata
            self.metadata["images"][image_metadata["id"]] = image_metadata
            self.metadata["stats"]["total_images"] += 1
            self._save_metadata()
            
            return {
                "success": True,
                "id": image_metadata["id"],
                "filename": filename,
                "local_url": f"/storage/images/{filename}",
                "thumbnail_url": f"/storage/images/thumbnails/{Path(thumbnail_path).name}" if thumbnail_path else None,
                "metadata": image_metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_image_from_data(self, image_data: bytes, prompt: str, extension: str = "png", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Save image from binary data"""
        try:
            # Generate filename
            filename = self._generate_filename("image", prompt, extension)
            file_path = self.images_path / filename
            
            # Save image
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            # Create thumbnail
            thumbnail_path = self._create_thumbnail(file_path)
            
            # Prepare metadata
            image_metadata = {
                "id": str(uuid.uuid4()),
                "filename": filename,
                "prompt": prompt,
                "file_path": str(file_path),
                "thumbnail_path": str(thumbnail_path) if thumbnail_path else None,
                "file_size": len(image_data),
                "created_at": datetime.now().isoformat(),
                "extension": extension,
                **(metadata or {})
            }
            
            # Add to metadata
            self.metadata["images"][image_metadata["id"]] = image_metadata
            self.metadata["stats"]["total_images"] += 1
            self._save_metadata()
            
            return {
                "success": True,
                "id": image_metadata["id"],
                "filename": filename,
                "local_url": f"/storage/images/{filename}",
                "thumbnail_url": f"/storage/images/thumbnails/{Path(thumbnail_path).name}" if thumbnail_path else None,
                "metadata": image_metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_thumbnail(self, image_path: Path, size: tuple = (256, 256)) -> Optional[Path]:
        """Create thumbnail for image"""
        try:
            # Create thumbnails directory
            thumbnails_dir = self.images_path / "thumbnails"
            thumbnails_dir.mkdir(exist_ok=True)
            
            # Open and resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                thumbnail_filename = f"thumb_{image_path.name}"
                thumbnail_path = thumbnails_dir / thumbnail_filename
                img.save(thumbnail_path, "JPEG", quality=85)
                
                return thumbnail_path
                
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def get_image_by_id(self, image_id: str) -> Optional[Dict[str, Any]]:
        """Get image metadata by ID"""
        return self.metadata["images"].get(image_id)
    
    def list_images(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """List images with pagination"""
        images = list(self.metadata["images"].values())
        # Sort by creation date (newest first)
        images.sort(key=lambda x: x["created_at"], reverse=True)
        return images[offset:offset + limit]
    
    def search_images(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search images by prompt"""
        results = []
        query_lower = query.lower()
        
        for image_data in self.metadata["images"].values():
            if query_lower in image_data["prompt"].lower():
                results.append(image_data)
        
        # Sort by creation date (newest first)
        results.sort(key=lambda x: x["created_at"], reverse=True)
        return results[:limit]
    
    def delete_image(self, image_id: str) -> bool:
        """Delete image and its metadata"""
        try:
            image_data = self.metadata["images"].get(image_id)
            if not image_data:
                return False
            
            # Delete files
            file_path = Path(image_data["file_path"])
            if file_path.exists():
                file_path.unlink()
            
            # Delete thumbnail
            if image_data.get("thumbnail_path"):
                thumbnail_path = Path(image_data["thumbnail_path"])
                if thumbnail_path.exists():
                    thumbnail_path.unlink()
            
            # Remove from metadata
            del self.metadata["images"][image_id]
            self.metadata["stats"]["total_images"] -= 1
            self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        stats = self.metadata["stats"].copy()
        
        # Calculate disk usage
        total_size = 0
        for path in [self.images_path, self.videos_path, self.audio_path]:
            if path.exists():
                for file_path in path.rglob("*"):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
        
        stats["total_disk_usage"] = total_size
        stats["total_disk_usage_mb"] = round(total_size / (1024 * 1024), 2)
        
        return stats
    
    def cleanup_old_files(self, days: int = 30) -> Dict[str, int]:
        """Clean up files older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = {"images": 0, "videos": 0, "audio": 0}
        
        # Clean up images
        for image_id, image_data in list(self.metadata["images"].items()):
            created_at = datetime.fromisoformat(image_data["created_at"])
            if created_at < cutoff_date:
                if self.delete_image(image_id):
                    deleted_count["images"] += 1
        
        return deleted_count

# Global storage manager instance
storage_manager = StorageManager()