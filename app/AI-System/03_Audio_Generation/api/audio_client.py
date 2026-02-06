import os
import wave
import base64
import google.generativeai as genai
from google.genai import types # Use new types from updated SDK if available, or fallback
from dotenv import load_dotenv

# Load Env
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class AudioGenerator:
    def __init__(self, model_name="gemini-2.5-flash-preview-tts"):
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        print(f"[CONNECTED] Audio Generator ({model_name})")

    def save_wave_file(self, filename, pcm_data):
        """Saves Raw PCM data to WAV."""
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(pcm_data)
        print(f"[SAVED] Audio saved to {filename}")

    def generate_speech(self, text, voice_name="Kore", output_path="output.wav"):
        """
        Single-speaker TTS.
        """
        try:
            # Construct config manually to ensure compatibility with py SDK versions
            config = genai.types.GenerationConfig(
                response_modalities=["AUDIO"],
                speech_config=genai.types.SpeechConfig(
                    voice_config=genai.types.VoiceConfig(
                        prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                )
            )
            
            response = self.model.generate_content(
                text,
                generation_config=config
            )
            
            # Extract Audio
            # Note: Structure might vary slightly based on SDK version (candidates[0].content.parts[0].inline_data.data)
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    self.save_wave_file(output_path, part.inline_data.data)
                    return output_path
            
            print("No audio data found in response.")
            return None

        except Exception as e:
            print(f"[ERROR] TTS Generation failed: {e}")
            return None

    def generate_podcast(self, transcript_prompt, speakers, output_path="podcast.wav"):
        """
        Multi-speaker TTS.
        speakers: List of dicts [{'name': 'Joe', 'voice': 'Kore'}, ...]
        transcript_prompt: Full string containing the conversation script including speaker names.
        """
        try:
            # Build Speaker Config
            speaker_configs = []
            for s in speakers:
                speaker_configs.append(
                    genai.types.SpeakerVoiceConfig(
                        speaker=s['name'],
                        voice_config=genai.types.VoiceConfig(
                            prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                                voice_name=s['voice']
                            )
                        )
                    )
                )

            config = genai.types.GenerationConfig(
                response_modalities=["AUDIO"],
                speech_config=genai.types.SpeechConfig(
                    multi_speaker_voice_config=genai.types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=speaker_configs
                    )
                )
            )

            response = self.model.generate_content(
                transcript_prompt,
                generation_config=config
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    self.save_wave_file(output_path, part.inline_data.data)
                    return output_path
            
            return None

        except Exception as e:
             print(f"[ERROR] Podcast Generation failed: {e}")
             return None

if __name__ == "__main__":
    client = AudioGenerator()
    print("Audio Generator Ready.")
