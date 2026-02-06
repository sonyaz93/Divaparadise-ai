import os
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class TextClient:
    def __init__(self, model_name="gemini-3-flash-preview", system_instruction=None):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        
        # Configure model with optional system instruction and tools
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )
        print(f"[CONNECTED] Text Generation Client ({model_name})")

    def generate_text(self, prompt, thinking_budget=None, temperature=1.0, tools=None, output_schema=None):
        """
        Generates text with optional Thinking Config, Tools, and Structured Output.
        Args:
            prompt (str): User input.
            thinking_budget (int): Thinking token budget.
            temperature (float): Creativity.
            tools (list): List of functions/tools.
            output_schema (dict): JSON Schema for structured output.
        """
        try:
            # Base Config
            config_args = {"temperature": temperature}

            # Add Thinking Config if requested
            if thinking_budget is not None:
                # Note: Using the raw dictionary structure for broad compatibility
                # or the specific types if available. SDK v0.1+ supports 'thinking_config'.
                # We use the typed helper if possible, else raw dict via **kwargs if needed.
                # Assuming updated SDK from context:
                
                # Check if we need to use 'thinking_level' (Gemini 3) or 'thinking_budget' (Gemini 2.5)
                # The user guide suggests using thinking_budget for 2.5 which is what we are likely targeting or 3-flash.
                
                # Dynamic construction to avoid import errors if types missing
                try:
                    t_config = genai.types.ThinkingConfig(include_thoughts=True)
                    if isinstance(thinking_budget, int):
                         t_config.thinking_budget = thinking_budget
                    
                    config_args["thinking_config"] = t_config
                except:
                    # Fallback or older SDK handling
                    print("[WARN] Thinking Config types not found, skipping thinking.")
                    pass

            # Add Tools if provided
            if tools:
                config_args["tools"] = tools

            # Add Structured Output if requested
            if output_schema:
                config_args["response_mime_type"] = "application/json"
                config_args["response_schema"] = output_schema

            # Note: 'tools' usually goes into the Model constructor or the generate_content call directly (as 'tools' param, not config).
            # The SDK behavior depends on version.
            # Standard way: model.generate_content(..., tools=tools)
            
            # We'll separate tools from config_args if passing as kwarg
            request_args = {
                "contents": prompt,
                "generation_config": genai.types.GenerationConfig(**config_args)
            }
            if tools:
                request_args["tools"] = tools

            response = self.model.generate_content(**request_args)
            
            # Check for thoughts in response
            # Some models return thought parts separately
            final_text = response.text
            
            # Simple check for Thoughts for debugging/lab use
            try:
                candidates = response.candidates[0].content.parts
                thoughts = [p.text for p in candidates if hasattr(p, 'thought') and p.thought]
                if thoughts:
                    return f"[THOUGHTS]\n{''.join(thoughts)}\n\n[ANSWER]\n{final_text}"
            except:
                pass

            return final_text

        except Exception as e:
            print(f"[ERROR] Text Generation failed: {e}")
            return None

    def start_chat(self, history=None, tools=None):
        """
        Starts a multi-turn chat session.
        Args:
            history (list): Chat history.
            tools (list): Tools to enable for this chat session. 
                          If provided, enable_automatic_function_calling is set to True.
        """
        return self.model.start_chat(
            history=history or [],
            enable_automatic_function_calling=bool(tools),
            tools=tools
        )

    def generate_with_image(self, prompt, image_path):
        """
        Multimodal generation: Text + Image context.
        """
        try:
            if not os.path.exists(image_path):
                return "Image file not found."
                
            # Note: In a real app we might use the internal FileManager or specific upload
            # For this simple client, we assume local processing if supported or upload.
            # Using the simplest approach for 'gemini-1.5-pro' which handles inputs well.
            
            # Placeholder for image loading logic (PIL or Upload)
            # Assuming 'google_studio_manager' style upload for production,
            # but here keeping it self-contained or assuming text-heavy focus.
            return "[Mock] Generated text based on image (Multimodal not fully linked in this isolated client)."
            
        except Exception as e:
    def create_cache(self, content, ttl_minutes=5):
        """
        Creates a context cache.
        Args:
            content (str): The massive text content to cache.
            ttl_minutes (int): Time to live in minutes.
        """
        try:
            # Note: Caching API interaction depends on specific SDK version.
            # Using standard 'genai.caching.CachedContent' pattern if available, or simulation.
            
            # Since we are using the standard 'google.generativeai', we look for caching.
            # If not available in this env, we print a simulation message.
            if hasattr(genai, 'caching'):
                print(f"[CACHE] Creating cache... ({len(content)} chars)")
                cache = genai.caching.CachedContent.create(
                    model=self.model_name,
                    display_name="project_cache",
                    system_instruction="You are an expert AI Analyst. You have access to the entire codebase.",
                    contents=[content],
                    ttl=datetime.timedelta(minutes=ttl_minutes),
                )
                print(f"[CACHE] Created: {cache.name}")
                return cache
            else:
                print("[WARN] Context Caching not supported in this SDK version. Simulating...")
                return content # Fallback to raw content
        except Exception as e:
             print(f"[ERROR] Cache creation failed: {e}")
             return None

    def generate_with_cache(self, prompt, cache):
        """
        Generates text using a cached context.
        """
        try:
            if hasattr(genai, "caching") and isinstance(cache, genai.caching.CachedContent):
                # Use the model linked to the cache
                model = genai.GenerativeModel.from_cached_content(cached_content=cache)
                response = model.generate_content(prompt)
                return response.text
            else:
                # Fallback: Just prepend the content (Long Context without Cache)
                full_prompt = f"CONTEXT:\n{cache}\n\nQUESTION:\n{prompt}"
                return self.generate_text(full_prompt)
        except Exception as e:
            return f"[ERROR] Cached Generation failed: {e}"

if __name__ == "__main__":
    client = TextClient()
    print(client.generate_text("Write a haiku about AI."))

if __name__ == "__main__":
    client = TextClient()
    print(client.generate_text("Write a haiku about AI."))
