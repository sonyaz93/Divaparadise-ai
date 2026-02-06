#!/usr/bin/env python3
"""
AI System API Server
Provides REST API endpoints for all AI-System modules
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add AI-System modules to path
sys.path.append(str(Path(__file__).parent))

# Import storage manager
from utils.storage_manager import storage_manager

# Pydantic Models
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "professional"
    size: Optional[str] = "1024x1024"
    quality: Optional[str] = "high"

class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 30
    style: Optional[str] = "cinematic"
    resolution: Optional[str] = "1080p"

class AudioGenerationRequest(BaseModel):
    prompt: str
    type: Optional[str] = "music"
    duration: Optional[int] = 60
    style: Optional[str] = "electronic"

class TextConversationItem(BaseModel):
    role: str
    content: str

class TextGenerationRequest(BaseModel):
    prompt: Optional[str] = None
    contents: Optional[list[TextConversationItem]] = None
    maxTokens: Optional[int] = 500
    temperature: Optional[float] = 0.7
    systemPrompt: Optional[str] = None

class EmbeddingRequest(BaseModel):
    text: str

# Initialize FastAPI app
app = FastAPI(
    title="Divaparadises AI System API",
    description="REST API for AI content generation and processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini for text generation
gemini_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI modules on startup"""
    global gemini_client
    
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    print(f"📡 AI Provider configured: {provider}")

    if provider == "gemini":
        try:
            # Initialize Gemini client
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                # Use gemini-2.5-flash-lite as suggested by user
                gemini_client = genai.GenerativeModel('gemini-2.5-flash-lite')
                print("✅ Gemini client (2.5-flash-lite) initialized successfully")
            else:
                print("⚠️  No Gemini API key found")
        except Exception as e:
            print(f"⚠️  Gemini initialization failed: {e}")
    elif provider == "ollama":
        print(f"🦙 Ollama provider selected. Model: {os.getenv('OLLAMA_MODEL', 'llama3')}")
        # Ollama doesn't need a specific client initialization here, we'll use requests/httpx
    else:
        print(f"⚠️  Unknown provider: {provider}. Falling back to mock mode.")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Image Generation
@app.post("/api/generate-image")
async def generate_image(request: ImageGenerationRequest):
    """Generate image using AI-System image generation module"""
    try:
        # Mock response for now - in real implementation, this would call actual AI service
        import hashlib
        seed = hashlib.md5(request.prompt.encode()).hexdigest()[:8]
        mock_url = f"https://picsum.photos/seed/{seed}/800/800"
        
        # Save the generated image to local storage
        save_result = storage_manager.save_image_from_url(
            url=mock_url,
            prompt=request.prompt,
            metadata={
                "style": request.style,
                "size": request.size,
                "quality": request.quality,
                "generation_type": "ai_generated",
                "model": "mock_generator"
            }
        )
        
        if save_result["success"]:
            return {
                "success": True,
                "url": mock_url,  # Original URL for immediate display
                "local_url": save_result["local_url"],  # Local stored URL
                "thumbnail_url": save_result["thumbnail_url"],
                "image_id": save_result["id"],
                "filename": save_result["filename"],
                "metadata": {
                    "mock": True, 
                    "style": request.style,
                    "size": request.size,
                    "quality": request.quality,
                    "stored_locally": True
                },
                "prompt": request.prompt
            }
        else:
            # Fallback if storage fails
            return {
                "success": True,
                "url": mock_url,
                "metadata": {
                    "mock": True, 
                    "style": request.style,
                    "size": request.size,
                    "quality": request.quality,
                    "storage_error": save_result.get("error")
                },
                "prompt": request.prompt
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Video Generation
@app.post("/api/generate-video")
async def generate_video(request: VideoGenerationRequest):
    """Generate video using AI-System video generation module"""
    try:
        # Mock response
        return {
            "success": True,
            "url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "metadata": {
                "mock": True, 
                "duration": request.duration,
                "style": request.style,
                "resolution": request.resolution
            },
            "prompt": request.prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Audio Generation
@app.post("/api/generate-audio")
async def generate_audio(request: AudioGenerationRequest):
    """Generate audio using AI-System audio generation module"""
    try:
        # Mock response
        return {
            "success": True,
            "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "metadata": {
                "mock": True, 
                "type": request.type,
                "duration": request.duration,
                "style": request.style
            },
            "prompt": request.prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Text Generation
@app.post("/api/generate-text")
async def generate_text(request: TextGenerationRequest):
    """Generate text using Gemini or Ollama with support for conversation history"""
    try:
        provider = os.getenv("AI_PROVIDER", "gemini").lower()
        
        # Prepare contents for AI API
        messages = []
        
        # System prompt handling
        system_instruction = request.systemPrompt or "You are a creative AI assistant for Divaparadises music platform."
        
        # Gemini logic
        if provider == "gemini" and gemini_client:
            gemini_contents = []
            if request.contents:
                for item in request.contents:
                    gemini_contents.append({
                        "role": "user" if item.role == "user" else "model",
                        "parts": [item.content]
                    })
            if request.prompt:
                gemini_contents.append({"role": "user", "parts": [request.prompt]})

            import google.generativeai as genai
            model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite', system_instruction=system_instruction)
            response = model.generate_content(
                gemini_contents,
                generation_config=genai.types.GenerationConfig(max_output_tokens=request.maxTokens, temperature=request.temperature)
            )
            return {
                "success": True,
                "text": response.text,
                "usage": {"tokens": len(response.text.split()), "model": "gemini-2.5-flash-lite-server"},
                "prompt": request.prompt or (request.contents[-1].content if request.contents else "")
            }

        # Ollama logic
        elif provider == "ollama":
            import requests
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
            
            # Format history for Ollama
            ollama_messages = [{"role": "system", "content": system_instruction}]
            if request.contents:
                for item in request.contents:
                    ollama_messages.append({"role": item.role, "content": item.content})
            if request.prompt:
                ollama_messages.append({"role": "user", "content": request.prompt})
            
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": ollama_model,
                    "messages": ollama_messages,
                    "stream": False,
                    "options": {
                        "num_predict": request.maxTokens,
                        "temperature": request.temperature
                    }
                },
                timeout=60 # Ollama can be slow on local hardware
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "text": data["message"]["content"],
                    "usage": {"tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0), "model": f"ollama-{ollama_model}"},
                    "prompt": request.prompt or (request.contents[-1].content if request.contents else "")
                }
            else:
                raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")

        # Fallback to Mock
        else:
            prompt_text = request.prompt or (request.contents[-1].content if request.contents else "Hello")
            return {
                "success": True,
                "text": f"Diva (Mock): ฉันได้รับข้อความว่า '{prompt_text}' แล้วค่ะ แต่ตอนนี้ AI Provider ({provider}) ไม่พร้อมทำงานค่ะ",
                "usage": {"tokens": 20, "model": "mock"},
                "prompt": prompt_text
            }
    except Exception as e:
        print(f"❌ Text Generation Error: {e}")
        return {
            "success": False,
            "error": str(e),
            "prompt": request.prompt
        }

# Document Analysis
@app.post("/api/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    options: str = '{"extractText": true, "summarize": true}'
):
    """Analyze document using AI-System document intelligence module"""
    try:
        options_dict = json.loads(options)
        
        # Mock response
        return {
            "success": True,
            "analysis": {
                "text": f"Mock document analysis for {file.filename}",
                "summary": "This is a mock summary of the document",
                "mock": True,
                "options": options_dict
            },
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Embeddings
@app.post("/api/embeddings")
async def create_embedding(request: EmbeddingRequest):
    """Create embeddings using AI-System embedding module"""
    try:
        # Mock embedding (random vector)
        import random
        random.seed(hash(request.text))  # Consistent for same text
        mock_embedding = [random.random() for _ in range(768)]
        
        return {
            "success": True,
            "embedding": mock_embedding,
            "dimensions": 768,
            "text": request.text,
            "mock": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Workflow endpoints
@app.post("/api/workflows/nano-banana")
async def run_nano_banana_workflow(request: dict):
    """Run Nano Banana workflow"""
    try:
        return {
            "success": True, 
            "result": {
                "workflow": "nano-banana",
                "input": request,
                "output": "Mock workflow result",
                "mock": True
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/workflows/veo-cinema")
async def run_veo_cinema_workflow(request: dict):
    """Run Veo Cinema workflow"""
    try:
        return {
            "success": True, 
            "result": {
                "workflow": "veo-cinema",
                "input": request,
                "output": "Mock video workflow result",
                "mock": True
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/workflows/podcast-studio")
async def run_podcast_studio_workflow(request: dict):
    """Run Podcast Studio workflow"""
    try:
        return {
            "success": True, 
            "result": {
                "workflow": "podcast-studio",
                "input": request,
                "output": "Mock audio workflow result",
                "mock": True
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# System info
@app.get("/api/system/info")
async def get_system_info():
    """Get AI-System information and capabilities"""
    return {
        "name": "Divaparadises AI System",
        "version": "1.0.0",
        "capabilities": [
            "Image Generation",
            "Video Generation", 
            "Audio Generation",
            "Text Generation",
            "Document Intelligence",
            "Embeddings & Search",
            "Workflow Automation",
            "Local Storage Management"
        ],
        "modules": {
            "gemini_client": gemini_client is not None,
            "storage_manager": True,
            "image_generator": False,  # Mock mode
            "video_generator": False,  # Mock mode
            "audio_generator": False,  # Mock mode
            "doc_processor": False,    # Mock mode
            "embedding_client": False  # Mock mode
        },
        "status": "operational",
        "mode": "development"
    }

# Storage Management Endpoints
@app.get("/api/storage/stats")
async def get_storage_stats():
    """Get storage statistics"""
    try:
        stats = storage_manager.get_storage_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/storage/images")
async def list_stored_images(limit: int = 50, offset: int = 0):
    """List stored images with pagination"""
    try:
        images = storage_manager.list_images(limit=limit, offset=offset)
        return {
            "success": True,
            "images": images,
            "count": len(images),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/storage/images/search")
async def search_stored_images(q: str, limit: int = 20):
    """Search stored images by prompt"""
    try:
        images = storage_manager.search_images(query=q, limit=limit)
        return {
            "success": True,
            "images": images,
            "query": q,
            "count": len(images)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/storage/images/{image_id}")
async def get_stored_image(image_id: str):
    """Get stored image by ID"""
    try:
        image_data = storage_manager.get_image_by_id(image_id)
        if image_data:
            return {"success": True, "image": image_data}
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/storage/images/{image_id}")
async def delete_stored_image(image_id: str):
    """Delete stored image"""
    try:
        success = storage_manager.delete_image(image_id)
        if success:
            return {"success": True, "message": "Image deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/storage/cleanup")
async def cleanup_old_files(days: int = 30):
    """Clean up files older than specified days"""
    try:
        deleted_count = storage_manager.cleanup_old_files(days=days)
        return {
            "success": True,
            "message": f"Cleaned up files older than {days} days",
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static file serving for stored images
from fastapi.staticfiles import StaticFiles

# Mount static files
storage_path = Path(__file__).parent / "storage"
if storage_path.exists():
    app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")

if __name__ == "__main__":
    print("🚀 Starting Divaparadises AI System API Server...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "api_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )